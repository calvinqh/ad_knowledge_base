'''
    A script that will upload entrez_ids_genesymbol.csv onto a mongo cluster.
    The script contains the function to upload the csv onto specific cluster
    This function, with modification, can be generalized for any csv file.

    Contains:
    upload_gene_information(db_ip:string, db_port:int)

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

'''
    The purpose of this function is to upload entrez_ids_genesymbol csv file to a Mongodb.
    The data is stored in the values db, in the gene collection
    @param db_ip:string, the ip of the mongodb
    @param db_port:int, the port of the mongodb
'''
def merge_gene_uniprot_information(mongo_conf):
    client = MongoClient(mongo_conf['host'], mongo_conf['port']) #Client used to connect to cluster
    db = client.values
    uniprot_collection = db.uniprot
    uniprots = uniprot_collection.find()
    gene_collection = db.gene
    genes = gene_collection.find()
    for doc in genes:
        uniprot_collection.update({'entrez_id':int(doc['entrez_id'])}, {'$set': {'gene_symbol':doc['gene_symbol']}}, multi=True, upsert=False)
        #print(type(doc['entrez_id']))


if __name__ == "__main__":
    merge_gene_uniprot_information(c.getMongoConfig())
