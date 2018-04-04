
# About the project
This project contains the tools needed to upload the provided data files (csv, xml, and txt) onto multiple databases. Patient information is stored onto a cassandra keyspace. RosmapRNA information is stored onto a mongo instance. Gene interaction information is stored onto a neo4j database. The tools to upload data onto these databases are located in ```tools/```.  Commands to upload the data without the python scripts are mentioned below.

The command line interface is ```adkb.py```

The available commands are listed below.
## Project Structure
```
ad_knowledge_base/
	__init__.py
	adkb.py
	models/
		__init__.py
		patient.py
	tools/
		__init__.py
		upload_patients.py
		upload_rnaseq.py
		upload_gene.py
		upload_interactors.py
	data/ #Add all csv,xml,and txt files here
```

## To upload data onto the databases
### Using python scripts
From the parent directory of ad_knowledge_base/ the following commands will upload data their databases
```python -m ad_knowledge_base.tools.upload_*```
Note: do not include the py extension when running the upload command.
### Using native NoSQL commands
#### Mongo ```(entrez_ids_uniprot.txt, )```

From the command line:
```
./mongoimport -d collection -c uniprot --type tsv --file entrez_ids_uniprot.txt --headerline
```
#### Cassandra```(patients.csv, )```
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
#### Neo4j```(PPI.csv, )```

In the neo4j conf file, disable the following line by adding a comment or setting the value to false. This will allow you to provide an absolute path to upload the csv.
```dbms.security.allow_csv_import_from_file_urls=true```

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
```python -m ad_knowledge_base.adkb```

## CLI commands
```
patient <name:string>
```
Retrieves all patient infromation.

