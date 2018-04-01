'''
    A script that will upload patients.csv onto a cassandra cluster keyspace.
    This script can be generalized for any csv file.

    Instructions: 
    User must set the server ip, port and keyspace for the cassandra cluster and keyspace.
    The user must also specify csv file they wish to upload.
    Each field in the csv will act as a column.
    Each row will become a record.
'''
from ..models.patient import Patient 

from cassandra.cqlengine.management import sync_table, drop_table
from cassandra.cqlengine import connection

import csv
import json

#database configs
server_ip = 'localhost'
keyspace = 'mylittlekeyspace'
port = 27017

#csv file configs
csv_file_name = 'ad_knowledge_base/data/patients.csv'  #The file where the data is read from
header = ['patient_id', 'age', 'gender', 'education'] #This is temprary (the values will be initalized later)


if __name__ == "__main__":


    #Create connection to server
    connection.setup([server_ip], "cqlengine", protocol_version=3)
    
    drop_table(Patient) #Drop table if it exist 
    sync_table(Patient) #In this case, it will create the table

    instance = {}
    csvFile = open(csv_file_name) #Load csvfile stream
    reader = csv.DictReader( csvFile ) #initalize csv reader with file stream
    header = reader.fieldnames #Contains the header of the csv (field/column names)

    #Insert each row into database
    for row in reader:
        for field in header:
            instance[field] = row[field]
        Patient.create(**instance)
