import pandas as pd
from py2neo import Graph, Node, Relationship, authenticate
from py2neo.packages.httpstream import http

from ..configs import DBConfig as c

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
