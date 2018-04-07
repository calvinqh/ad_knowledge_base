'''
    A script that will merge gene collection gene symbol name into
    uniprot collection that is all on a mongo cluster in the values database.
    The script contains the function "merge" these two collection 

    Contains:
    merge_uniprot_gene_information(mongo_conf:dict)

    Preqs/Instructions: 
    The user must set the mongo configurations in the configs file
    This program assumes that gene and uniprot collection in the values database
        are filled with the correct documents (user ran upload_gene and upload_uniprot
'''
from pymongo import MongoClient

from ..configs import DBConfig as c

'''
    This function adds gene_symbol field into all docs in uniprot collection
    It utilizes the gene collection to get the gene symbols for each uniprot doc
    @param mongo_conf:dict, the configuration of the mongo db (host and port)
'''
def merge_uniprot_gene_information(mongo_conf):
    client = MongoClient(mongo_conf['host'], mongo_conf['port']) #Client used to connect to cluster
    db = client.values
    uniprot_collection = db.uniprot
    uniprots = uniprot_collection.find()
    gene_collection = db.gene
    genes = gene_collection.find()
    for doc in genes:
        uniprot_collection.update_many({'entrez_id':int(doc['entrez_id'])}, {'$set': {'gene_symbol':doc['gene_symbol']}}, upsert=False)
        #print(type(doc['entrez_id']))


if __name__ == "__main__":
    merge_uniprot_gene_information(c.getMongoConfig())
