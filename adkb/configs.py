class DBConfig:
    
    @staticmethod
    def getMongoConfig():
        conf = {
                'host':'0.0.0.0',
                'port':27017
        }
        
        return conf

    @staticmethod
    def getCassandraConfig():
        conf = {
            'host':'0.0.0.0',
            'default_keyspace':'cqlengine'
        }
        return conf

    @staticmethod
    def getNeo4JConfig():
        conf = {
            'user':'neo4j',
            'pw':'1',
            'host':'0.0.0.0',
            'http_port':11001,
            'db_name':'PPI',
            'graph_name':'interactors'
        }
        return conf
