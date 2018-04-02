'''
    The CLI for the user to query the ad knowledge base.
'''

'''
    Returns the average expression values for AD/MCI/NCI for the given entrez id
    @param entrez, the entrez id 
'''

from pymongo import MongoClient
server_ip = 'localhost'
port = 27017

client = MongoClient(server_ip, port)

'''
    Given the entrez id for a gene
    Return the mean and std of the expression values for AD/MCI/NCI
    @param entrez:int, the id of the gene mean will be calculated for
    @return dict, the mean and std for AD, MCI and NCI
'''
def getGeneReport(entrez):
    db = client.values #use client to retrieve values database
    collection = db.rna #retrieve reference to rna collection
    
    cursors = [] #contian cursor to all aggregate query results
    
    #References to labels, the database saves label information in the form of numbers
    disease_labels = {
        '1': 'NCI',
        '(2,3)': 'MCI',
        '(4,5)': 'AD',
        '6': 'Other dementia'
    }

    #Each query filters collection by disease label number
    for key,value in disease_labels.items():

        #For keys that are tuples, match stage requires $or operator
        match_by_tuple = False
        if len(key) > 1:
            match_by_tuple = True
        if(match_by_tuple):
            cursors.append(collection.aggregate([
                {
                    '$match': { #filter documents that match the following
                        "$or": [
                            {
                                "DIAGNOSIS": key[0], #search with first label key
                                "DIAGNOSIS": key[1]  #search with second label key
                            } 
                        ]
                    }
                },
                {
                    '$group': { #how aggreate will be formated
                        '_id':value, #disease name
                        'avg_entrez': { '$avg': '$'+str(entrez)}, #calc average
                        'std_entrez': { '$stdDevPop': '$'+str(entrez)} #calc std by popu
                    }
                }
            ]))
        else:
            cursors.append(collection.aggregate([
                {
                    '$match': { #filter documents that match the following
                        "DIAGNOSIS": key #search by label key
                    }
                },
                {
                    '$group': { #how the aggregate will be formated
                        '_id':value, #disease name
                        'avg_entrez': { '$avg': '$'+str(entrez)}, #calc avg
                        'std_entrez': { '$stdDevPop': '$'+str(entrez)} #calc std by popu
                    }
                }
            ]))

    #create dictionary maping disease name to aggregate results
    result = {}
    for cursor in cursors:
        for doc in cursor:
            result[doc['_id']] = doc #_id contains the disease name
    return result
    

def mainloop():
    while(True):
        cmd = input(">>")


if __name__ == "__main__":
    getGeneReport(197322)  
    #mainloop()
