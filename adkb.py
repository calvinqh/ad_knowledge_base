from models.patient import Patient

from cassandra.cqlengine import connection

from pymongo import MongoClient


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

    '''
        Returns a dict containing information about patients
        @param p_id:int, the patient id
        @return dict, a dict containing patient infromation
                    <patient_id, age, gender, education, diagnosis>
    '''
    def getPatientReport(self,p_id):
        db = self.mongo_client.values
        rosmap_collection = db.rna
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
        pass

    '''
        Returns information about a specific gene given gene_symbol.
        @param gene_symbol: The gene symbol for a gene
        @return doc/dict, general information about a gene
    '''
    def geteGeneDetails(self,gene_symbol):
        pass

    '''
        Uploads and retrieves all genes that interact with the given gene
        @param gene_interactors:dataframe, relationship between genes (interactions)
        @param gene:string, the entrez id of a gene
        @param all_genes:collection, a mongo collection containing information about genes
    '''
    def n_order_genes(self,gene_interactors, gene, all_genes):
        pass

    '''
        Searches for entrez id given gene name and mongo gene collection
        @param id:int, the entrez id of a gene
        @param all_genes:mongo collection, the colletion containing docs with gene info
        @return string, gene name for corresponding entrez id
    '''
    def find_id(self,gene, all_genes):
        pass

    '''
        Searches for gene name given entrez id of gene and mongo gene collection
        @param id:int, the entrez id
        @param all_genes:mongo_collection, the collection containing docs with gene info
        @return string, gene name for corresponding entrez id
    '''
    def find_name(self,id, all_genes):
        pass



