# API Documentation
## Class
```
class adkb.ADKnowledgeBase(mongo_configs, cassnadra_configs, neo_configs)
```
Initializes an interface instance with connections to mongo, cassandra and neo4j instances.

## Instance based methods
From ADKnowledgeBase instance:

```
getNOrderGenes(entrez_id, order)
```
Returns a dict of entrez_ids connected to the given entrez id. Maps orders to list of entrez ids
```
getGeneReport(entrez_id)
```
Returns mean and std expression values for the given gene
```
display_gene_information(entrez_id)
```
Returns gene information in a dictionary (symbols, name, ids, and corresponding uniprots)
```
getPatientReport(patient_id)
```
Returns patient information in a dictionary (id, age, gender, education, diagnosis)
```
display_norder_genes(entrez_id,order)
```
Display the entrez ids of the genes and their order that connect to the provided entrez id
```
display_gene_report(entrez_id)
```
Displays mean and std of expression values for the given entrez id in standard output
```
display_patient_report(patient_id)
```
Display patient information in standard output (id, age, gender, education, diagnosis)



