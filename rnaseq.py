from pymongo import MongoClient
import csv
import json

#database configs
server_ip = 'localhost'
port = 27017

#csv file configs
csv_file_name = 'data/ROSMAP_RNASeq_entrez.csv'
header = ["PATIENT_ID", "DIAGNOSIS"]


if __name__ == "__main__":

    client = MongoClient(server_ip, port)
    csvFile = open(csv_file_name)
    reader = csv.DictReader( csvFile )
    header = reader.fieldnames
    #print(header)
    #count = 10

    db = client.values
    collection = db.rna
    collection.drop()

    for each in reader:
        '''
        if(count < 0):
            break
        count-=1
        '''
        row = {}
        for field in header:
            row[field] = each[field]

        collection.insert(row)

