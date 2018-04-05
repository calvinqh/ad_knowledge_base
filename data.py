import pandas as pd
import cassandra
import numpy as np

from pymongo import Connection
from py2neo import Graph, Node, Relationship

#puts all pairs of interactors which has a specific gene in it into a neo4j graph so that one interactor will have multiple relationships
#then prints out all genes with a relationship with the specific gene
def n_order_genes(gene_interactors, gene, all_genes):
    #connect to local neo4j server with password set as '1'
    graph = Graph(password = '1')
    interact = graph.begin()
    a = gene_interactors["interactor_A"]
    b = gene_interactors["interactor_B"]

    #goes through the pandas document from beginning to end
    for i in range(a.shape[0]):
        interactor_a = str(a[i])
        interactor_b = str(b[i])
        #if the specific gene is found, make a relationship of the pair
        if interactor_a == gene or interactor_b == gene:
            first = Node("interactor", name = interactor_a)
            second = Node("interactor", name = interactor_b)
            graph.merge(Relationship(first, "INTERACTS WITH", second))

    #prints out all the related genes of the given gene
    print ""
    print "INTERACTING GENES:"
    for i in graph.match(rel_type = "INTERACTS WITH"):
        if i.start_node()["name"] == str(gene):
            print find_name(i.end_node()["name"], all_genes)
        elif i.end_node()["name"] == str(gene):
            print find_name(i.start_node()["name"], all_genes)


#puts the gene name and entrez id of the gene into a mongodb collection
#def make_gene_table(entrez_and_genes):
#    #connect to local mongodb server
#    connect = Connection('localhost', 27017)
#    db = connect.collection
#    all_genes = db.all_genes
#    ids = entrez_and_genes["entrez_id"]
#    genes = entrez_and_genes["gene_symbol"]
#
#    #goes through the pandas document from beginning to end
#    #to insert the data, and if the program is ran again,
#    #it doesn't make duplicates since insert command doesn't
#    #care if there are duplicates or not
#    print "Inserting data into MongoDB. . ."
#    for i in range(ids.shape[0]):
#        all_genes.update({'entrez':str(ids[i]), 'gene':genes[i]}, {'entrez':str(ids[i]), 'gene':genes[i]}, upsert = True)
#
#    return all_genes

#finds the associated entrez id of a given gene
def find_id(gene, all_genes):
    row = all_genes.find({"gene_symbol":gene})
    gene_id = gene
    for name in list(row):
        gene_id = name["entrez_id"]

    return gene_id

#finds the associated gene of a given entrez id
def find_name(id, all_genes):
    row = all_genes.find({"entrez_id":int(id)})
    gene = id
    for name in list(row):
        gene = name["gene_symbol"]

    return gene

def print_pinfo(p_info, pid):
    row = p_info.find({'id':pid})
    for name in list(row):
        print name["age"]
        print name["gender"]
        print name["education"]
        print name["diagnosis"]
    
def merge_entrez_uniprot(entrez_and_genes, uniprot):

    entrez = entrez_and_genes['entrez_id']
    gene = entrez_and_genes['gene_symbol']
    for i in range(entrez.shape[0]):
        eid = entrez[i].astype(np.int32)
        print i
        uniprot.update({'entrez_id':eid},{'$set': {'gene_symbol':gene[i]}}, multi = True, safe = True)

def find_gene_info(gene, uniprot):

    print 'Gene INFO:'
    name = uniprot.find({'gene_symbol':gene})
    entrez = ""
    for info in list(name):
        entrez = info['entrez_id']
    print "entrez ID: ", entrez

    row = uniprot.find({'entrez_id':entrez})
    for info in list(row):
        print "uniprot ID: ", info['uniprot_id']
        print "Full Gene name: ", info['Gene Name']

def main():

    print("Enter [1] to find all n-order interacting genes of a GENE")
    print("Enter [2] to find the mean and std of a GENEs expression values for AD/MCI/NCI")
    print("Enter [3] to find all other information associated with a GENE")
    print("Enter [4] to find all information of a given PATIENT")
    print("Enter [5] to QUIT")
    print("")

    connect = Connection('localhost', 27017)
    db = connect.collection
    uniprot = db.uniprot
    all_genes = db.all_genes

    press = int(input("ENTER A NUMBER FROM 1-4: "))

    if press == 1:
        gene_interactors = pd.read_csv("PPI.csv")
        entrez_and_genes = pd.read_csv("entrez_ids_genesymbol.csv")
        gene = raw_input("ENTER A GENE: ")
        #all_genes = make_gene_table(entrez_and_genes)
        find_more = True

        while find_more == True:
            gene_num = find_id(gene, all_genes)
            interacting_genes = n_order_genes(gene_interactors, gene_num, all_genes)

            print "Enter [0] to go BACK"
            print "Enter [1] to enter a different GENE"
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
        entrez_and_genes = pd.read_csv("entrez_ids_genesymbol.csv")
        merge_entrez_uniprot(entrez_and_genes, uniprot)

        gene = raw_input("ENTER A GENE: ")
        find_gene_info(gene, uniprot)

    elif press == 4:
        diseases = pd.read_csv("ROSMAP_RNASeq_disease_label.csv")
        patient_RNA = pd.read_csv("ROSMAP_RNASeq_entrez.csv")
        patients = pd.read_csv("patients.csv")

        pid = raw_input("ENTER A PATIENT ID: ")

        #p_info = make_p_table(patients, patient_RNA, diseases)
        #print_pinfo(p_info, pid)

if __name__ == "__main__":
    main()
