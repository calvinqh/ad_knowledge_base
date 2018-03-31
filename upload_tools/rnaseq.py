'''
    A script that will upload ROSMAP_RNASeq_entrez.csv onto a mongo cluster.
    This script can be generalized for any csv file.

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

#database configs
server_ip = 'localhost'
port = 27017

#csv file configs
csv_file_name = 'data/ROSMAP_RNASeq_entrez.csv'
header = ["PATIENT_ID", "DIAGNOSIS"] #This is temporary (the values will be initalized later)


if __name__ == "__main__":

    client = MongoClient(server_ip, port) #Client used to connect to cluster

    csvFile = open(csv_file_name) #Load csvfile stream
    reader = csv.DictReader( csvFile ) #initalize csv reader with file stream
    header = reader.fieldnames #Contain the header of the csv (field names)

    db = client.values  #retrieve the database Values on the cluster
    collection = db.rna #retrieve the collection RNA from Values database
    collection.drop() #empty the collection (drop all documents)

    #For each row in the csv, convert it into json format and insert into the collection
    for each in reader:
        #create json form of row
        row = {}
        for field in header:
            row[field] = each[field]

        #upload onto collection
        collection.insert(row)

