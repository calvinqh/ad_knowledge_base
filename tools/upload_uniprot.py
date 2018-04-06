'''
    A script that will upload entrez_ids_uniprot.txt onto a mongo cluster.
    The script contains the function to upload the txt onto specific cluster
    This function, with modification, can be generalized for any txt file.
    The database is values
    The collection is called uniprot
    
    Contains:
    upload_uniprot_info(mongo_conf:dict)

    Preqs/Instructions: 
    The user has setup the mongo configuratiosn in teh configs file
    Assumes:
        The user has mongoimport installed.
        The txt file is located in teh data folder
        The user is runnign this program from the parent directory
            of this projecty
        Mongo cluset and database is running and setup
        Mongo configs are correct, else will crash
        The database is called uniprot
'''
from pymongo import MongoClient
import csv
import json
import re
import bson
import subprocess

from ..configs import DBConfig as c

'''
    Upload entrez_ids_uniprot txt file to a Mongodb.
    This function executes a subprocess onto the command line.
    This subprocess calls mongoimport command
    The data is stored in the values db, in the uniprot collection
    ASsumes:
        The user has mongoimport installed.
        The user is running this function from the parent directory
            of this project
        The txt file is lcoated in the data folder
        The mongo configs are correct, else will crash
        Mongo server is up and running
    @param mongo_conf:dict, the configs for the mongodb (ip and port) check configs
'''
def upload_uniprot_info(mongo_conf):

    txt_file_name = 'ad_knowledge_base/data/entrez_ids_uniprot.txt'
    queryTemplate = '''
        mongoimport -h {} -p {} -d values -c uniprot --type tsv --file {} --headerline
    '''
    query = queryTemplate.format(mongo_conf['host'],mongo_conf['port'],txt_file_name)
    subprocess.call(query,shell=True)
    
    
if __name__ == "__main__":
    upload_uniprot_info(c.getMongoConfig())
