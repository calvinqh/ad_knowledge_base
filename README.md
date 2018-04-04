

# About the project
This project contains the tools needed to upload the provided data files (csv, xml, and txt) onto multiple databases to create a Alzheimer Disease Knowledgebase. This project also contains an interface to interact with these databases. The interface provides methods to query the database for information. Patient information is stored onto a cassandra keyspace. RosmapRNA information is stored onto a mongo instance. Gene interaction information is stored onto a Neo4J database. The tools to upload data onto these databases are located in ```tools/```.  Instructions on how to upload the data with/without python scripts are mentioned below.

The command line interface is ```cli.py```

The available commands are listed below.
## Setup
1. Create a virtual environment for this project. [link to instructions](http://virtualenvwrapper.readthedocs.io/en/latest/command_ref.html)
```
mkvirtualenv <ve name> 
workon <ve name>
```
2. Install the python requirements for this project
```
pip install -r requirements.txt
```
3. Skip this step if you already have the databases setup. If not, I will be assumming that you have mongodb  apache cassandra, and neo4j desktop installed. Download and installation instructions detaield here:
[Mongodb](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-linux/)
[Cassandra](http://cassandra.apache.org/download/)
[Neo4J](https://neo4j.com/docs/operations-manual/current/installation/linux/tarball/)
**Note**: I recommend you use Neo4J desktop version. Deploying a local database is easier.

4. Setup the database configs for Mongo,Cassandra, and Neo4J. In the ```configs.py``` file. Edit the config functions to match your database configs.
5. In the ```data/``` folder at the root of this project, put all csv, xml, and txt files that are required for this project.
6. To perform uploads rerfer to upload instructions below.
7. To start the command line interface:
```pythom -m ad_knowledge_base.cli```


## Project Structure
```
ad_knowledge_base/
	__init__.py
	adkb.py 					#The interface module
	configs.py					#Database configs
	models/						#Model used by Cassandra database
		__init__.py
		patient.py
	tools/
		__init__.py
		upload_patients.py		#Upload script for patients.csv
		upload_rnaseq.py		#Upload script for ROSMAP_RNASeq_entrez.csv
		upload_gene.py			#Upload script for entrez_ids_genesymbol.csv
		upload_interactors.py	#Upload script for PPI.csv
	data/ 						#Add all csv,xml,and txt files here
```

## To upload data onto the databases
### Using python scripts
From the parent directory of ad_knowledge_base/ the following commands will upload data their databases
```python -m ad_knowledge_base.tools.upload_*```
Note: do not include the py extension when running the upload command.
### Using native NoSQL commands
#### Mongo ```(entrez_ids_uniprot.txt, ROSMAP_RNASeq_entrez.csv, uniprot-human.xml)```

From the command line:
```
./mongoimport -d collection -c uniprot --type tsv --file entrez_ids_uniprot.txt --headerline
```
#### Cassandra```(patients.csv)```
Run ```./cqlsh``` and in the shell:
```
CREATE KEYSPACE patient_info
  WITH REPLICATION = { 
   'class' : 'SimpleStrategy', 
   'datacenter1' : 1 
} ; 
CREATE TABLE patient ( 
   patient_id text PRIMARY KEY,
   age int,
   education text,
   gender text
) ;
COPY patient_info.patient FROM '<RELATIVE PATH TO CSV>/patients.csv' WITH HEADER=true;
```
#### Neo4J```(PPI.csv)```

In the neo4j conf file, disable the following line by adding a comment or setting the value to false. This will allow you to provide an absolute path to upload the csv.
```#dbms.directories.import=import```

If you did not disable this feature, you will have to put the csv file into the import folder of the database folder.

To upload **PPI.csv**,assuming you have turned off the feature
```
	USING PERIODIC COMMIT
	LOAD CSV FROM 'file:///<path/to/csv>/PPI.csv' AS row#alternatively file:///PPI.csv

	MERGE(p1:interactor {name: row[0]})
	MERGE(p2:interactor {name: row[1]})
	MERGE((p1)-[:INTERACTS_WITH]->(p2));
```


## To run the command line interface
From parent directory of ad_knowledge_base/ the following command will run a cli program to query the databases.
```python -m ad_knowledge_base.cli```

## CLI commands
```
patient <name:string>
```
Retrieves all patient infromation.


## Data structure
![](docs/dataflow.png)

