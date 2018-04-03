from models.patient import Patient

from cassandra.cqlengine import connection

from pymongo import MongoClient

def getPatientReport(_id):
    #Connection setup
    connection.setup(['localhost'], "cqlengine", protocol_version=3)

    mongo_client = MongoClient('localhost', 27017)
    db = mongo_client.values
    rosmap_collection = db.rna

    #Search cassandra for patient record
    patient = None
    try:
        patient = Patient.get(patient_id=_id)
        print("Patient found.")
    except:
        print("Patient does not exist.")
    
    print(patient.items())
    
    #Search for corresponding rosmap doc for patient
    rosmap_cursor = rosmap_collection.find({'PATIENT_ID':_id})
    patient_doc = rosmap_cursor.next()

    patient_information = {}
    for key,value in patient.items():
        patient_information[key] = value
    patient_information['diagnosis'] = patient_doc['DIAGNOSIS']
    print(patient_information)
    return patient_information
    

if __name__ == '__main__':
    getPatientReport('X690_120604')
    #getPatientReport('X690_10604')
