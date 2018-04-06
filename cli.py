from adkb import ADKnowledgeBase
from configs import DBConfig as c

def main():
    kb = ADKnowledgeBase(c.getMongoConfig(), c.getCassandraConfig(), c.getNeo4JConfig())
    exit = False
    while(not exit):
        print("Enter [1] to find all n-order interacting genes of a GENE")
        print("Enter [2] to find the mean and std of a GENEs expression values for AD/MCI/NCI")
        print("Enter [3] to find all other information associated with a GENE")
        print("Enter [4] to find all information of a given PATIENT")
        print("Enter [5] to QUIT")
        print("")

        press = int(input("ENTER A NUMBER FROM 1-4: "))

        if press == 1:
            input_gene = input("ENTER A GENE: ")
            #all_genes = make_gene_table(entrez_and_genes)
            find_more = True

            while find_more:
                gene_num = kb.find_id(input_gene)
                interacting_genes = kb.getNOrderGenes(gene_num)
                print(interacting_genes)
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
                print(kb.getGeneReport(gene_num))

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
                print(kb.getPatientReport(input_patient_id))
                print("Enter [0] to go BACK")
                print("Enter [1] to enter a different GENE")
                again = int(input("ENTER [0/1]   "))
                while again != 1 and again != 0:
                    again = int(input("Ener [0/1] "))
                if again == 0:
                    find_more = False
                elif again == 1:
                    input_patient_id = input("ENTER PATIENT ID: ")
        elif press == 5:
            exit = True


if __name__ == "__main__":
    main()

