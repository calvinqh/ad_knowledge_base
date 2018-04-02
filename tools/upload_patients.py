'''
    A script that will upload patients.csv onto a cassandra cluster keyspace.
    This script can be generalized for any csv file.

    Instructions: 
    User must set the server ip, port and keyspace for the cassandra cluster and keyspace.
    The user must also specify csv file they wish to upload.
    Each field in the csv will act as a column.
    Each row will become a record.
    
    To Create a keyspace, use cqlsh:
    CREATE KEYSPACE IF NOT EXISTS mylittlekeyspace WITH REPLICATION = 
    {'class': 'SimpleStrategy', 'replication_factor' : 1};
'''
from ..models.patient import Patient 

from cassandra.cqlengine.management import sync_table, drop_table
from cassandra.cqlengine import connection

import csv
import json

#database configs
server_ip = 'localhost'
port = 27017

'''
    The purpose of this function is to upload patients csv to Cassandra keyspace
    The keyspace is specified in the Patient model. (To change update patient model)
    In this case, the keyspace is 'mylittlekeyspace'
    @param db_ip:string, the ip of the Cass database
    @param db_port:string, the port of the Cass database
'''
def upload_patient_information(db_ip, db_port='0000'):
    connection.setup([server_ip], "cqlengine", protocol_version=3)
    
    drop_table(Patient) #Drop table if it exist 
    sync_table(Patient) #In this case, it will create the table

    csv_file_name = 'ad_knowledge_base/data/patients.csv'  #The file where the data is read from

    csvFile = open(csv_file_name) #Load csvfile stream
    reader = csv.DictReader( csvFile ) #initalize csv reader with file stream
    header = reader.fieldnames #Contains the header of the csv (field/column names)

    #Insert each row into database
    instance = {}
    for row in reader:
        for field in header:
            instance[field] = row[field]
        Patient.create(**instance)


if __name__ == "__main__":
    upload_patient_information(server_ip)
