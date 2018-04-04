from models.patient import Patient

from cassandra.cqlengine import connection

from pymongo import MongoClient

from py2neo import Graph, authenticate
from py2neo.packages.httpstream import http

'''
    A interface to retrieve information about Alzheimer Disease Knowledge Base
'''
class ADKnowledgeBase:

    '''
        Initalizes the connection to mongo, cassandra, and neo databases
        @param mongo_conf:dict, dict containing ip and port of mongo database
        @param cass_conf:dict, dict containing cluster and default keyspace of cass database
        @param neo_conf:dict, dict containing neo configs
    '''
    def __init__(self, mongo_conf, cass_conf, neo_conf):
        #Create mongo client
        self.mongo_client = MongoClient(mongo_conf['ip'],mongo_conf['port'])
        #Setup default connection to cassandra cluster
        connection.setup([cass_conf['ip']],cass_conf['default_keyspace'], protocol_version=3)
        #setup connection to neo4j database
        self.neo_client = None
        self.setup_neo(neo_conf)

    def setup_neo(self, conf):
        http.socket_timeout = 10000000
       
        user = conf['user']
        pw = conf['pw']
        host = conf['host']
        port = conf['http_port']
        db = conf['db_name']
        graph = conf['graph_name']

        auth_uri = '{}:{}'.format(host,port)
        authenticate(auth_uri, user, pw)

        db_uri = 'http://{}:{}@{}:{}/{}/{}'.format(user,pw,host,port,db,graph)
        self.graph = Graph(db_uri, bolt=False)

    '''
        Returns a dict containing information about patients
        @param p_id:int, the patient id
        @return dict, a dict containing patient infromation
                    <patient_id, age, gender, education, diagnosis>
    '''
    def getPatientReport(self,p_id):
        db = self.mongo_client.values #Retrieve db reference from client
        rosmap_collection = db.rna #Retrieve collection from db
        
        #Search cassandra fro patient record
        patient = None
        try:
            patient = Patient.get(patient_id=p_id)
            print("Patient found.")
        except:
            print("Patient does not exist.")

        #print(patient.items())
        
        #Search for corresponding rosmap doc for patient
        rosmap_cursor = rosmap_collection.find({'PATIENT_ID':p_id})
        patient_doc = rosmap_cursor.next()

        #Create a dict containing patient information
        patient_information = {}
        #Read information from cassandra results
        for key,value in patient.items():
            patient_information[key] = value
        #read diagnosis information from mongo results
        patient_information['diagnosis'] = patient_doc['DIAGNOSIS']

        return patient_information

    '''
        Given the entrez id for a gene
        Return the mean and std of the expression values for AD/MCI/NCI
        @param entrez:int, the entrez id of a gene
        @return dict, the mean and std for AD, MCI, and NCI
    '''
    def getGeneReport(self,entrez):
        db = self.mongo_client.values #use client to retrieve values database
        collection = db.rna #retrieve reference to rna collection
        
        cursors = [] #contian cursor to all aggregate query results
        
        #References to labels, the database saves label information in the form of numbers
        disease_labels = {
            '1': 'NCI',
            '(2,3)': 'MCI',
            '(4,5)': 'AD',
            '6': 'Other dementia'
        }

        #Each query filters collection by disease label number
        for key,value in disease_labels.items():

            #For keys that are tuples, match stage requires $or operator
            match_by_tuple = False
            if len(key) > 1:
                match_by_tuple = True
            if(match_by_tuple):
                cursors.append(collection.aggregate([
                    {
                        '$match': { #filter documents that match the following
                            "$or": [
                                {
                                    "DIAGNOSIS": key[0], #search with first label key
                                    "DIAGNOSIS": key[1]  #search with second label key
                                } 
                            ]
                        }
                    },
                    {
                        '$group': { #how aggreate will be formated
                            '_id':value, #disease name
                            'avg_entrez': { '$avg': '$'+str(entrez)}, #calc average
                            'std_entrez': { '$stdDevPop': '$'+str(entrez)} #calc std by popu
                        }
                    }
                ]))
            else:
                cursors.append(collection.aggregate([
                    {
                        '$match': { #filter documents that match the following
                            "DIAGNOSIS": key #search by label key
                        }
                    },
                    {
                        '$group': { #how the aggregate will be formated
                            '_id':value, #disease name
                            'avg_entrez': { '$avg': '$'+str(entrez)}, #calc avg
                            'std_entrez': { '$stdDevPop': '$'+str(entrez)} #calc std by popu
                        }
                    }
                ]))

        #create dictionary maping disease name to aggregate results
        result = {}
        for cursor in cursors:
            for doc in cursor:
                result[doc['_id']] = doc #_id contains the disease name
        return result
     
    '''
        Returns information about a specific gene given gene_symbol.
        @param gene_symbol: The gene symbol for a gene
        @return doc/dict, general information about a gene
    '''
    def getGeneDetailsBySymbol(self,gene_symbol):
        db = self.mongo_client.values #retrieve reference to values database from client
        collection = db.gene #retrieve reference to collection from database

        cursor = collection.find({"gene_symbol":gene_symbol})
        
        #return the result of the collection query search
        for doc in cursor:
            #print(doc)
            return doc
        return None

    '''
        Returns information about a specific gene given entrez_id.
        @param entrez_id:string The entrez id for a gene
        @return doc/dict, general information about a gene
    '''
    def getGeneDetailsByEntrez(self,entrez_id):
        db = self.mongo_client.values #retrieve reference to values database from client
        collection = db.gene #retrieve reference to collection from database

        cursor = collection.find({"entrez_id":entrez_id})
        
        #return the result of the collection query search
        for doc in cursor:
            #print(doc)
            return doc
        return None



    '''
        Uploads and retrieves all genes that interact with the given gene
        @param gene:string, the entrez id of a gene
        @param all_genes:collection, a mongo collection containing information about genes
        @return list, a list containing all genes that interact with the given gene
    '''
    def getNOrderGenes(self, gene):
        interactors = []
        #Search for genes that interact with the given entrez_id
        for i in self.graph.match(rel_type = "INTERACTS_WITH"):
            if i.start_node()['name'] == gene:
                print(i.start_node['name'])
                interactors.append(find_name(i.end_node()["name"]))
            elif i.end_node()['name'] == gene:
                print(i.end_node['name'])
                interactors.append(find_name(i.start_node()['name']))
        return interactors

    '''
        Searches for entrez id given gene symbol 
        @param id:int, the entrez id of a gene
        @return string, gene name for corresponding entrez id
    '''
    def find_id(self,gene):
        doc = self.getGeneDetailsBySymbol(gene_symbol)
        if doc is not None:
            return doc['entrez_id']
        return None

    '''
        Searches for gene name given entrez id of gene
        @param entrez_id:int, the entrez id
        @return string, gene symbol for corresponding entrez id
    '''
    def find_name(self,entrez_id):
        doc = self.getGeneDetailsByEntrez(entrez_id)
        if doc is not None:
            return doc['gene_symbol']
        return None
