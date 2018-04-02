import pandas as pd

from py2neo import Graph, Path, Node, Relationship

'''
    Return all genes that have a interaction with the given gene (entrez id)
    @param gene_interactors:dataframe, the relationship between interacting genes
    @param gene:string, the entrez id we want to find the interacting genes for
    @return list, the list of entrez ids that interact with the given gene (entrez id) 
'''
def n_order_genes(gene_interactors, gene):
    graph = Graph(password = '1')
    interact = graph.begin()
    a = gene_interactors["interactor_A"] #Contains the series interactor A
    b = gene_interactors["interactor_B"] #Contains the series interactor B
    n_order = [] #Contains all genes interacting with the given gene
    i = 0 #Index of interacting pair

    for i in range(a.shape[0]):
        interactor_a = str(a[i]) 
        interactor_b = str(b[i])
        if interactor_a == gene or interactor_b == gene:
            first = Node("interactor", name = interactor_a)
            second = Node("interactor", name = interactor_b)

            graph.merge(Relationship(first, "INTERACTS WITH", second))

            #insert the gene that interacts with the given gene
            if interactor_a == gene:
                n_order.insert(i, interactor_b)
                i = i+1
                #print interactor_b
            elif interactor_b == gene:
                n_order.insert(i, interactor_a)
                i = i+1
                #print interactor_a

    #print("NUMBER OF GENES INTERACTING WITH {0}: {1}".format(gene, n))
    return n_order

'''
    Return the gene id associated with the given gene name
    @param entrez_and_genes:dataframe, information about genes
    @param gene:string, the gene we want to find the entrez id for
    @return string, the entrez id for the given gene
'''
def gene_id(entrez_and_genes, gene):
    name = gene.upper()
    id = entrez_and_genes["entrez_id"]
    genes = entrez_and_genes["gene_symbol"]

    for i in range(id.shape[0]):
        if genes[i].upper() == name:
            return str(id[i])

    return ""

'''
    Display the corresponding gene symbol for the given entrez id list (gene id)
    @param entrez_and_genes:dataframe, information about genes (entrez_id, gene symbol ...)
    @param g_ids:list, a list of entrez ids (gene ids) that will have their symbol displayed
    @return None
'''
def gene_name(entrez_and_genes, g_ids):
    id = entrez_and_genes["entrez_id"]
    genes = entrez_and_genes["gene_symbol"]

    for i in range(id.shape[0]):
        for k in range(len(g_ids)):
            if str(id[i]) == g_ids[k]:
                print str(genes[i])

    
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
        gene = input("ENTER A GENE: ")
        gene_num = gene_id(entrez_and_genes, gene)
        interacting_genes = n_order_genes(gene_interactors, gene_num)

        print ""
        print "INTERACTING GENES:"
        gene_name(entrez_and_genes, interacting_genes)


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
