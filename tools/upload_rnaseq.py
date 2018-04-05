'''
    A script that will upload ROSMAP_RNASeq_entrez.csv onto a mongo cluster.
    The script contains the function to upload the csv onto specific cluster
    This function, with modification, can be generalized for any csv file.

    Contains:
    upload_rosmaprna(db_ip:string, db_port:int)

    Instructions: 
    User must set the server ip and port for the mongo cluster.
    The user must also specify csv file they wish to upload.
    The data will be uploaded in json format. 
    Each field in the csv will act as a key.
    Each row will become a document.
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
    The purpose of this function is to upload ROSMAP_RNASeq_entrez csv to Mongodb
    The data is stored in the values db, in the rna collection
    @param db_ip:string, the ip of the mongodb
    @param db_port:int, the port of the mongodb
'''
def upload_rosmaprna(mongo_conf):
    client = MongoClient(mongo_conf['host'], mongo_conf['port']) #Client used to connect to cluster

    csv_file_name = 'ad_knowledge_base/data/ROSMAP_RNASeq_entrez.csv'

    csvFile = open(csv_file_name) #Load csvfile stream
    reader = csv.DictReader( csvFile ) #initalize csv reader with file stream
    header = reader.fieldnames #Contain the header of the csv (field names)

    db = client.values  #retrieve the database Values on the cluster
    collection = db.rna #retrieve the collection RNA from Values database
    collection.drop() #empty the collection (drop all documents)
    
    #For each row in the csv, convert it into json format and insert into the collection
    for row in reader:
        instance = {}
        #create json form of row
        for field in header:
            if (re.match("^\d+?\.\d+?$", row[field]) is not None):
                instance[field] = float(row[field])
            else:
                instance[field] = row[field]

        #upload onto collection
        collection.insert(instance)


if __name__ == "__main__":
    upload_rosmaprna(c.getMongoConfig())
