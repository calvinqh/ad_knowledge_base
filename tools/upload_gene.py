'''
    A script that will upload entrez_ids_genesymbol.csv onto a mongo cluster.
    The script contains the function to upload the csv onto specific cluster
    This function, with modification, can be generalized for any csv file.
    The database is value
    The collection is called gene

    Contains:
    upload_gene_information(mongo_conf:dict)

    Instructions:
    The user has setup the mongo configurations in the configs file
    Assumes:
        The csv file is located in the the data folder
        The user is running the program from the parent directory
            of this project
        Mongo cluster and database is running and setup
        Mongo configs are correct, else wil crash
        Thet database is called gene
'''
from pymongo import MongoClient
import csv
import json
import re
import bson

from ..configs import DBConfig as c

#database configs
server_ip = 'localhost'
port = 27017

'''
    Upload entrez_ids_genesymbol csv file to a Mongodb.
    The data is stored in the values db, in the gene collection
     Assumes:
        The csv file is located in the the data folder
        The user is running this function from the parent directory
            of this project
        Mongo cluster and database is running and setup
        Mongo configs are correct, else wil crash
        The database is called gene
    @param mongo_conf:dict, the configs for the mongodb(ip,port) check configs
'''
def upload_gene_information(mongo_conf):
    client = MongoClient(mongo_conf['host'], mongo_conf['port']) #Client used to connect to cluster

    csv_file_name = 'ad_knowledge_base/data/entrez_ids_genesymbol.csv'

    csvFile = open(csv_file_name) #Load csvfile stream
    reader = csv.DictReader( csvFile ) #initalize csv reader with file stream
    header = reader.fieldnames #Contain the header of the csv (field names)

    db = client.values  #retrieve the database Values on the cluster
    collection = db.gene #retrieve the collection RNA from Values database
    collection.drop() #empty the collection (drop all documents)
    
    #For each row in the csv, convert it into json format and insert into the collection
    for row in reader:
        instance = {}
        #create json form of row
        for field in header:
            instance[field] = row[field]

        #upload onto collection
        collection.insert(instance)


if __name__ == "__main__":
    upload_gene_information(c.getMongoConfig())
