'''
    A script that will upload patients.csv onto a cassandra cluster keyspace.
    This script can be generalized for any csv file.

    Instructions: 
    User must set the server ip, port and keyspace for the cassandra cluster and keyspace.
    The user must also specify csv file they wish to upload.
    Each field in the csv will act as a column.
    Each row will become a record.
'''
from cassandra.cluster import cluster
import csv
import json

#database configs
server_ip = 'localhost'
keyspace = 'mylittlekeyspace'
port = 27017

#csv file configs
csv_file_name = 'data/patients.csv'  #The file where the data is read from
new_table_name = 'test'              #table name where the data will be inserted
header = ["PATIENT_ID", "DIAGNOSIS"] #This is temprary (the values will be initalized later)


if __name__ == "__main__":

    cluster = Cluster(server_ip)    #Cluster reference
    session = cluster.connect(keyspace) #Session reference to specific key space


    #TODO: clear the table data
    #collection.drop()

    #Upload csv file into specified table name
    session.execute("""
        COPY %table_name FROM %csv_file_name WITH HEADER=true;
        """,
        {'table_name':table_name, 'csv_file_name':csv_file_name}
    )

    """
    
    

    """