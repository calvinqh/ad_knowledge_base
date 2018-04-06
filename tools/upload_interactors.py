'''
    A script that will upload PPI.csv 
    The script contains the function to upload the csv to a neo4j database
    The graph and database names are provided by the users config

    Contains:
    upload_gene_interactions(neo_conf:dict)

    Preqs/Instructions: 
    The user must set the neo4j configurations in the configs file
    Assumes:
        The csv file is located in the data folder
        That the user is running this program from the parent
            directory of this project.
        Neo4J database and graph is running and up
        Neo configs are correct, with crash otherwise
'''

import pandas as pd
from py2neo import Graph, Node, Relationship, authenticate
from py2neo.packages.httpstream import http

from ..configs import DBConfig as c

'''
    Will upload PPI.csv information into a neo4j database.
    The database configs must be given to this function.
    Assumes:
        Neo configs are correct, other wise it will crash
        User calls this function from the parent directory
            of this project
        The csv file is located in the data folder
        The neo database config has turned off dbms.directories.import=import
    @param neo_conf:dict, configuration of the neo4j database.
'''

def upload_gene_interactions(neo_conf):
   
    http.socket_timeout = 10000000
   
    user = neo_conf['user']
    pw = neo_conf['pw']
    host = neo_conf['host']
    port = neo_conf['http_port']
    db = neo_conf['db_name']
    graph = neo_conf['graph_name']

    auth_uri = '{}:{}'.format(host,port)
    authenticate(auth_uri, user, pw)

    db_uri = 'http://{}:{}@{}:{}/{}/{}'.format(user,pw,host,port,db,graph)
    g = Graph(db_uri, bolt=False)
   
    query = '''
        USING PERIODIC COMMIT
        LOAD CSV FROM 'file:///home/calvin/Documents/bigdata/ad_knowledge_base/data/PPI.csv' AS row

        MERGE (p1:interactor {name: row[0]})
        MERGE (p2:interactor {name: row[1]})

        MERGE((p1)-[:INTERACTS_WITH]->(p2));
    '''
    g.run(query).dump()



if __name__ == "__main__":
    upload_gene_interactions(c.getNeo4JConfig())
