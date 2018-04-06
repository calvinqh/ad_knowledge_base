'''
    A script that will upload ROSMAP_RNASeq_entrez.csv onto a mongo cluster.
    The script contains the function to upload the csv onto specific cluster
    This function, with modification, can be generalized for any csv file.
    The database is values
    The collection is called rna

    Contains:
    upload_rosmaprna(mongo_conf:dict)

    Preqs/Instructions: 
    The user has setup the mongo configurations in the configs file
    Assumes:
        The csv file is located in the data folder
        The user is running this program from the parent directory
            of this project
        Mongo cluster and database is running and setup
        Mongo configs are correct, else will crash
        The database is called values
'''
from pymongo import MongoClient
import csv
import re
import json

from ..configs import DBConfig as c

'''
    Upload ROSMAP_RNASeq_entrez csv to Mongodb
    The data is stored in the values database, in the rna collection
    Assumes:
        The user is runnign this function from the parent directory
            of this project
        The csv file is located in the data folder
        The mongo configs are correct, else will crash
        The mongo server is up and running
    @param mongo_conf:dict, configs for the mongodb (ip and port) check configs
'''
def upload_rosmaprna(mongo_conf):
    client = MongoClient(mongo_conf['host'], mongo_conf['port']) #Client used to connect to cluster

    csv_file_name = 'adkb/data/ROSMAP_RNASeq_entrez.csv'

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
