import pandas as pd

def main():

    entrez_and_genes = pd.read_csv("entrez_ids_genesymbol.csv")
    patients = pd.read_csv("patients.csv")
    gene_interactors = pd.read_csv("PPI.csv")
    diseases = pd.read_csv("ROSMAP_RNASeq_disease_label.csv")
    patient_RNA = pd.read_csv("ROSMAP_RNASeq_entrez.csv")

    get_data(entrez_and_genes, session)
    get_patient(patients, patient_RNA, diseases, session)

    for index, row in entrez_and_genes.iterrows():
        print(row)

if __name__ == "__main__":
    main()
