from BioSQL import BioSeqDatabase
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import sqlite3
from Bio.Seq import Seq

# Variavel para os caminhos 
protein_file = "/home/hppp123/IC/SCPT/analisePAN/Orthogrups_teste/OP_{id_grupo}.fas"
cds_file = "/home/hppp123/IC/SCPT/analisePAN/Orthogrups_teste/OCDS_{id_grupo}.fas"


minSeq4Commit = 10

#Conectar com o banco de dado 
db_file = "mybiosql.db"
con = sqlite3.connect(db_file)
cursor = con.cursor()

# Consulta para recuperar os grupos de ortólogos com mais de 4 sequências
orthogroup_consulta = '''
SELECT id_grupo
FROM orthogrups
GROUP BY id_grupo
HAVING COUNT(id_protein) > 4
'''

cursor.execute(orthogroup_consulta)
orthogroup_results = cursor.fetchall()

#print("Orthogroup IDs com mais de 4 seq:")
#print(orthogroup_results)

for orthogroup in orthogroup_results:
    id_grupo = orthogroup[0]
    #print(f"Orthogrupo a ser processado: {id_grupo}")

    # Consulta para recuperar os identificadores de proteínas do grupo
    protein_consulta = '''
    SELECT sequences_protein.id, sequences_protein.sequence
    FROM orthogrups
    INNER JOIN sequences_protein ON orthogrups.id_protein = sequences_protein.id '''

    cursor.execute(protein_consulta)
    protein_results = cursor.fetchall()

    #print(f"Protein Sequences for Orthogroup {id_grupo}:")
    #print(protein_results) 

    protein_records = []

    countSeq =  0

    for result in protein_results:
        id_protein, sequence = result
        record = SeqRecord(Seq(sequence), id=str(id_protein), description=str(id_protein))
        protein_records.append(record)
        countSeq +=1
        if countSeq % minSeq4Commit ==0: 
             con.commit()

    #print(f"NUmero de Record de Proteinas: {len(protein_records)}")  

    # Escrever as sequências de proteínas no arquivo
    protein_file = f"/home/hppp123/IC/SCPT/analisePAN/Orthogrups_teste/OP_{id_grupo}.fas"
    with open(protein_file, 'w') as protein_fasta:
        SeqIO.write(protein_records, protein_fasta, 'fasta')

    cds_consulta = '''
    SELECT sequences_cds.id, sequences_cds.sequence
    FROM orthogrups
    INNER JOIN sequences_cds ON orthogrups.id_protein = sequences_cds.id
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
        if countSeq % minSeq4Commit ==0:
            con.commit()

    #print(f"Numero de Record de CDS: {len(cds_records)}")

    # Escrever as sequências de CDS no arquivo
    cds_file = f"/home/hppp123/IC/SCPT/analisePAN/Orthogrups_teste/OCDS_{id_grupo}.fas"
    with open(cds_file, 'w') as cds_fasta:
        SeqIO.write(cds_records, cds_fasta, 'fasta')
        
con.commit()
con.close()

