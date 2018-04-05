class DBConfig:
    
    @staticmethod
    def getMongoConfig():
        conf = {
                'host':'localhost',
                'port':27017
        }
        
        return conf

    @staticmethod
    def getCassandraConfig():
        conf = {
            'host':'localhost',
            'default_keyspace':'cqlengine'
        }
        return conf

    @staticmethod
    def getNeo4JConfig():
        conf = {
            'user':'neo4j',
            'pw':'1',
            'host':'localhost',
            'http_port':11001,
            'db_name':'PPI',
            'graph_name':'interactors'
        }
        return conf
