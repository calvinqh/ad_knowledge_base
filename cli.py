from adkb.adkb import ADKnowledgeBase
from adkb.configs import DBConfig as c
from adkb.tools.upload_interactors import upload_gene_interactions
from adkb.tools.upload_gene import upload_gene_information 
from adkb.tools.upload_patients import upload_patient_information 
from adkb.tools.upload_rnaseq import upload_rosmaprna
from adkb.tools.upload_uniprot import upload_uniprot_info
from adkb.tools.merge_uniprot_gene import merge_uniprot_gene_information

def main():
    kb = ADKnowledgeBase(c.getMongoConfig(), c.getCassandraConfig(), c.getNeo4JConfig())
    exit = False
    while(not exit):
        display_menu()
        press = int(input("ENTER A NUMBER FROM 0-10: "))

        if press == 1:
            input_gene = input("ENTER A GENE: ")
            #all_genes = make_gene_table(entrez_and_genes)
            find_more = True

            while find_more:
                gene_num = kb.find_id(input_gene)
                kb.display_norder_genes(gene_num,1) 
                print()
                print("Enter [0] to go BACK")
                print("Enter [1] to enter a different GENE")
                again = int(input("Enter [0/1]   "))
                #Check for valid input option
                while again != 1 and again != 0:
                    again = int(input("Enter [0/1]   "))
                if again == 0:
                    find_more = False
                elif again == 1:
                    input_gene = input("ENTER A GENE: ")

        elif press == 2:
            input_gene = input("ENTER A GENE: ")
            find_more = True
            while find_more:
                gene_num = kb.find_id(input_gene)
                kb.display_gene_report(gene_num)
                print()
                print("Enter [0] to go BACK")
                print("Enter [1] to enter a different GENE")
                again = int(input("Enter [0/1]   "))
                while again != 1 and again != 0:
                    again = int(input("Enter [0/1] "))
                if again == 0:
                    find_more = False
                elif again == 1:
                    input_gene = input("ENTER A GENE: ")
        elif press == 3:
            input_gene = input("ENTER A GENE: ")
            find_more = True
            while find_more:
                kb.display_gene_info(input_gene)
                print()
                print("Enter [0] to go BACK")
                print("Enter [1] to enter a different GENE")
                again = int(input("Enter [0/1]   "))
                while again != 1 and again != 0:
                    again = int(input("Enter [0/1] "))
                if again == 0:
                    find_more = False
                elif again == 1:
                    input_gene = input("ENTER A GENE: ")

        elif press == 4:
            input_patient_id = input("ENTER PATIENT ID: ")
            find_more = True
            while find_more:
                kb.display_patient_report(input_patient_id)
                print()
                print("Enter [0] to go BACK")
                print("Enter [1] to enter a different PATIENT ID")
                again = int(input("ENTER [0/1]   "))
                while again != 1 and again != 0:
                    again = int(input("Ener [0/1] "))
                if again == 0:
                    find_more = False
                elif again == 1:
                    input_patient_id = input("ENTER PATIENT ID: ")
        elif press == 5:
            #insert PPI
            print("Uploading....")
            upload_gene_interactions(c.getNeo4JConfig())
            print("Complete..!")
        elif press == 6:
            #insert gene
            print("Uploading....")
            upload_gene_information(c.getMongoConfig())
            print("Complete..!")
        elif press == 7:
            #insert patients
            print("Uploading....")
            upload_patient_information(c.getCassandraConfig())
            print("Complete..!")
        elif press == 8:
            #insert RosmapRna_entrez
            print("Uploading....")
            upload_rosmaprna(c.getMongoConfig())
            print("Complete..!")
        elif press == 9:
            #insert uniprot
            print("Uploading....")
            upload_uniprot_info(c.getMongoConfig())
            print("Complete..!")
        elif press == 10:
            #merge uniprot and gene
            print("Merging....")
            merge_uniprot_gene_information(c.getMongoConfig())
            print("Complete..!")
        elif press == 0:
            exit = True

def display_menu():
    print()
    print()
    print("===Commands Available===")
    print("Enter [0] to QUIT")
    print("Enter [1] to find all n-order interacting genes of a GENE")
    print("Enter [2] to find the mean and std of a GENEs expression values for AD/MCI/NCI")
    print("Enter [3] to find all other information associated with a GENE")
    print("Enter [4] to find all information of a given PATIENT")
    print("Enter [5] to UPLOAD PPI.csv")
    print("Enter [6] to UPLOAD entrez_id_genesymbol.csv")
    print("Enter [7] to UPLOAD patients.csv")
    print("Enter [8] to UPLOAD ROSMAP_RNASeq_entrez.csv")
    print("Enter [9] to UPLOAD entrez_ids_uniprot.txt")
    print("Enter [10] to MERGE gene symbols into uniprot")
    print("")



if __name__ == "__main__":
    main()

