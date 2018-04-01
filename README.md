# About the project
This project contains the tools needed to upload the provided data files (csv, xml, and txt) onto multiple databases. Patient information is stored onto a cassandra keyspace. RosmapRNA information is stored onto a mongo instance. Gene interaction information is stored onto a neo4j database. The tools to upload data onto these databases are located in ```tools/```. 

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
		upload_rna.py
	data/
```

## To upload data onto the databases
From the parent directory of ad_knowledge_base/the following commands will upload data their databases
```python -m ad_knowledge_base.tools.upload_*```
Note: do not include the py extension when running the upload command.

## To run the command line interface
From parent directory of ad_knowledge_base/ the following command will run a cli program to query the databases.
```python -m ad_knowledge_base.adkb```

## CLI commands
```
patient <name:string>
```
Retrieve all patient infromation.

