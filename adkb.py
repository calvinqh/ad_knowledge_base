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

def getGeneAverage(entrez):
    db = client.values
    collection = db.rna
    x = collection.aggregate([
        {
            '$match': {
                "DIAGNOSIS": "NA"
            }
        },
        {
            '$group': {
                '_id':"null",
                'avg_entrez': { '$avg': '$'+str(entrez) }
            }
        }
    ])
    for doc in x:
        print(doc)

    

def mainloop():
    while(True):
        cmd = input(">>")


if __name__ == "__main__":
    getGeneAverage(197322)  
    #mainloop()
