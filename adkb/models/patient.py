from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

class Patient(Model):
    __keyspace__ = 'patient_info' #tells which keyspace to store this model in

    #List of model fields
    patient_id = columns.Text(primary_key=True)
    age = columns.Integer()
    gender = columns.Text()
    education = columns.Text()
