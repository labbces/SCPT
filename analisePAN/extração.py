from BioSQL import BioSeqDatabase
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import sqlite3
from Bio.Seq import Seq

# Variavel para os caminhos 
#I am commenting the folloing three lines as they are not being used.
#seq_CDS = "/Storage/data1/hellen.silva/db-extraction/Orthogrups_CDS/{orthogroup}.cds.fa"
#seq_OP = "/Storage/data1/hellen.silva/db-extraction/Orthogrups_Proteinas/{orthogroup}.fa"
#orthogrups_tvs = "/Storage/data1/hellen.silva/db-extraction/arquivos_db/Orthogroups_for_longest_trans.tsv"


minSeq4Commit = 10

#Conectar com o banco de dado 
db_file = "mybiosql.db"
con = sqlite3.connect(db_file)
cursor = con.cursor()

# Consulta para recuperar os grupos de ortólogos com mais de 4 sequências
orthogroup_consulta = '''
SELECT orthogroup
FROM orthogrups
GROUP BY orthogroup
HAVING COUNT(id_protein) > 3
'''

cursor.execute(orthogroup_consulta)
orthogroup_results = cursor.fetchall()

#print("Orthogroup IDs com mais de 4 seq:")
print(orthogroup_results)

for orthogroup in orthogroup_results:
    orthogroup = orthogroup[0]
    #print(f"Orthogrupo a ser processado: {orthogroup}")

    # Consulta para recuperar os identificadores de proteínas do grupo
    protein_consulta = f'''
    SELECT sequences_protein.id, sequences_protein.sequence
    FROM orthogrups
    INNER JOIN sequences_protein ON orthogrups.id_protein = sequences_protein.id
    WHERE orthogrups.orthogroup = '{orthogroup}'
    '''


    cursor.execute(protein_consulta)
    protein_results = cursor.fetchall()

    #print(f"Sequencias de proteinas Orthogroup {orthogroup}:")


    protein_records = []

    countSeq =  0

    for result in protein_results:
        id_protein, sequence = result
        record = SeqRecord(Seq(sequence), id=str(id_protein), description=str(id_protein))
        protein_records.append(record)
        countSeq +=1
        #As we are not writing to the DB, we do not need to commit, so I am commenting the following two lines
        #if countSeq % minSeq4Commit ==0: 
        #     con.commit()

    #print(f"Numero de Record de Proteinas: {len(protein_records)}")  

    # Escrever as sequências de proteínas no arquivo
    protein_file = f"/Storage/data1/hellen.silva/db-extraction/Orthogrups_Proteinas/{orthogroup}.fa"
    with open(protein_file, 'w') as protein_fasta:
        SeqIO.write(protein_records, protein_fasta, 'fasta')

    cds_consulta = f'''
    SELECT sequences_cds.id, sequences_cds.sequence
    FROM orthogrups
    INNER JOIN sequences_cds ON orthogrups.id_protein = sequences_cds.id
    WHERE orthogrups.orthogroup = '{orthogroup}'
    '''

    cursor.execute(cds_consulta)
    cds_results = cursor.fetchall()

    cds_records = []

    countSeq =  0

    # SeqRecord para as sequências de CDS
    for result in cds_results:
        id_cds, sequence = result
        record = SeqRecord(Seq(sequence), id=str(id_cds), description=str(id_cds))
        cds_records.append(record)
        countSeq +=1
        #As we are not writing to the DB, we do not need to commit, so I am commenting the following two lines
        #if countSeq % minSeq4Commit ==0:
        #    con.commit()

    #print(f"Numero de Record de CDS: {len(cds_records)}")

    # Escrever as sequências de CDS no arquivo
    cds_file = f"/Storage/data1/hellen.silva/db-extraction/Orthogrups_CDS/{orthogroup}.cds.fa"
    with open(cds_file, 'w') as cds_fasta:
        SeqIO.write(cds_records, cds_fasta, 'fasta')
        
con.commit()
con.close()

