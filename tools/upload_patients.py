'''
    A script that will upload patients.csv onto a cassandra cluster keyspace.
    The script contains a function to upload the csv onto a Cass cluster keyspace
    This function, with modification, can be generalized for any csv file.

    Contains:
    upload_patient_information(cass_conf:dict)

    Instructions: 
    The user must set the cassandra configurations in the configs file
    Assumes:
        The csv file is in the data folder.
        The cassandra configs are correct, will crash otherwise
        The keyspace and database are up and running
            Other wise check readme for instructions on cassandra db
            and keyspace setup
        The user is running this program from the parent directory
            of this project
'''
from ..models.patient import Patient 

from cassandra.cqlengine.management import sync_table, drop_table
from cassandra.cqlengine import connection

import csv
import json

from ..configs import DBConfig as c

#database configs
server_ip = 'localhost'
port = 27017

'''
    Uploads patients csv to Cassandra keyspace
    The keyspace is specified in the Patient model. (To change update patient model
        and update keyspace using cqlsh)
    In this case, the keyspace is 'patient_info'
    Assumes:
        Neo configs are correct, otherwise will crash
        User calls this function from parent directory of this project
        Csv file located in data folder
        Cassandra database is running.
    @param cass_conf:dict, config of cassandra database. check configs file. 
'''
def upload_patient_information(cass_conf):
    connection.setup([cass_conf['host']], cass_conf['default_keyspace'], protocol_version=3)
    
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
    upload_patient_information(c.getCassandraConfig())
