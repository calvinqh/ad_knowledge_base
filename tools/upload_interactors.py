import pandas as pd
from py2neo import Graph, Node, Relationship, authenticate
from py2neo.packages.httpstream import http

def upload_gene_interactions(conf):
   
    http.socket_timeout = 10000000
   
    user = conf['user']
    pw = conf['pw']
    host = conf['host']
    port = conf['http_port']
    db = conf['db_name']
    graph = conf['graph_name']

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
    user = 'neo4j'
    password = '1'
    host = 'localhost'
    http_port = 11018
    db_name = 'PPI'
    graph_name = 'interactors'
    neo_conf = {'user':user,'pw':password,'host':host,'http_port':http_port,'db_name':db_name, 'graph_name':graph_name}
    
    upload_gene_interactions(neo_conf)
