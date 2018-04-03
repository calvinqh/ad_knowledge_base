import pandas as pd
import cassandra

from pymongo import Connection
from py2neo import Graph, Node, Relationship

'''
    Displays all genes that that have a interaction with the given gene (entrez id)
    @param gene_interactors:dataframe, the relationship between interacting genes
    @param gene:string, the entrez id we want to find the interacting genes for
    @param all_genes:collection, a mongo collection containing information about genes
    @return None.
'''
def n_order_genes(gene_interactors, gene, all_genes):
    graph = Graph(password = '1')
    interact = graph.begin()
    a = gene_interactors["interactor_A"] #Contains the series interactor A
    b = gene_interactors["interactor_B"] #Contains the series interactor B

    #Upload gene interactor data onto Neo4j database
    for i in range(a.shape[0]):
        interactor_a = str(a[i]) 
        interactor_b = str(b[i])
        if interactor_a == gene or interactor_b == gene:
            first = Node("interactor", name = interactor_a)
            second = Node("interactor", name = interactor_b)
            graph.merge(Relationship(first, "INTERACTS WITH", second))

    #Search for genes that interactor with the given gene
    print ""
    print "INTERACTING GENES:"
    #Loop through every edge/relationship with the tag INTERACTS WITH
    for i in graph.match(rel_type = "INTERACTS WITH"):
        if i.start_node()["name"] == gene: #If node1 matches gene
            print find_name(i.end_node()["name"], all_genes) 
        elif i.end_node()["name"] == gene: #If node 2 matches gene
            print find_name(i.start_node()["name"], all_genes)

'''
    Uploads entrez and gene name / symbol onto a mongo database
    @param entrez_and_genes:dataframe, a dataframe containing information about
                                        entrez ids, gene name, gene symbol
    @return mongo_collection, a reference to the collection with entrez and gene information 
'''
def make_gene_table(entrez_and_genes):

    connect = Connection('localhost', 27017)
    db = connect.collection
    all_genes = db.all_genes #reference to collection to gene information
    ids = entrez_and_genes["entrez_id"] #reference entrez id series
    genes = entrez_and_genes["gene_symbol"] #reference gene series
    print "Inserting data into MongoDB..."
    #Insert into databse, if duplicates exists update duplicate
    for i in range(ids.shape[0]):
        all_genes.update({'entrez':str(ids[i]), 'gene':genes[i]}, {'entrez':str(ids[i]), 'gene':genes[i]}, upsert = True)

    return all_genes

'''
    Searches for entrez id given gene name and mongo gene collection.
    @param gene:string, the gene name the function is searching for
    @param all_genes:mongo collection, the collection search is performed on
    @return int, the corresponding entrez id for the gene
'''
def find_id(gene, all_genes):
    row = all_genes.find({"gene":gene})
    for name in list(row):
        gene_id = name["entrez"]

    return gene_id

'''
    Searches for gene name given entrez id of gene and mongo gene collection
    @param id:int, the entrez id
    @param all_genes:mongo_collection, the collection containing docs with gene info
    @return string, gene name for corresponding entrez id
'''
def find_name(id, all_genes):
    row = all_genes.find({"entrez":id})
    gene = id
    for name in list(row):
        gene = name["gene"]

    return gene

    
'''
    CLI driver to retrieve information
'''
def main():

    print("Press [1] to find all n-order interacting genes of a GENE")
    print("Press [2] to find the mean and std of a GENEs expression values for AD/MCI/NCI")
    print("Press [3] to find all information associated with a GENE")
    print("Press [4] to find all information of a given PATIENT")
    print("")

    press = int(input("PRESS A NUMBER FROM 1-4: "))

    if press == 1:
        gene_interactors = pd.read_csv("PPI.csv")
        entrez_and_genes = pd.read_csv("entrez_ids_genesymbol.csv")
        gene = raw_input("ENTER A GENE: ")
        all_genes = make_gene_table(entrez_and_genes)
        find_more = True

        while find_more == True:
            gene_num = find_id(gene, all_genes)
            interacting_genes = n_order_genes(gene_interactors, gene_num, all_genes)

            print "Press[0] to go BACK"
            print "Press [1] to enter a different GENE"
            again = int(input("Enter [0/1]   "))
            while again != 1 and again != 0:
                again = raw_input("Enter [0/1]   ")
            if again == 0:
                find_more = False
            elif again == 1:
                gene = raw_input("ENTER A GENE: ")


    elif press == 2:
        diseases = pd.read_csv("ROSMAP_RNASeq_disease_label.csv")
        patient_RNA = pd.read_csv("ROSMAP_RNASeq_entrez.csv")
    elif press == 3:
        patient_RNA = pd.read_csv("ROSMAP_RNASeq_entrez.csv")
        patients = pd.read_csv("patients.csv")
    elif press == 4:
        entrez_and_genes = pd.read_csv("entrez_ids_genesymbol.csv")

    #for index, row in entrez_and_genes.iterrows():
    #    print(row)

if __name__ == "__main__":
    main()
