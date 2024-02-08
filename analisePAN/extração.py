from BioSQL import BioSeqDatabase
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import sqlite3
from Bio.Seq import Seq

# Variavel para os caminhos 
protein_file = "/home/hppp123/IC/orto_protein.fas"
cds_file = "/home/hppp123/IC/orto_CDS.fas"

minSeq4Commit = 10

#Conectar com o banco de dado 
db_file = "mybiosql.db"
con = sqlite3.connect(db_file)
cursor = con.cursor()

#Consulta para recuperar as sequencias de proteinas e CDS
protein_consulta = '''
SELECT sequences_protein.id, sequences_protein.sequence
FROM orthogrups
INNER JOIN sequences_protein ON orthogrups.id_protein = sequences_protein.id
'''

cursor.execute(protein_consulta)
protein_results = cursor.fetchall()

# SeqRecord para sequencia de proteinas 
protein_records = []

for result in protein_results:
    id_protein, sequence = result
    #print("ID Protein:", id_protein)
    #print("Sequence:", sequence)
    record = SeqRecord(Seq(sequence), id=str(id_protein), description=str(id_protein))
    protein_records.append(record)

#Escrever as sequencias nos arquivos 
with open(protein_file, 'w') as protein_fasta:
    countSeq = 0
    for record in protein_records:
     SeqIO.write(protein_records, protein_fasta, 'fasta')
     countSeq += 1
     if countSeq % minSeq4Commit  == 0:
        con.commit()


cds_consulta = '''
SELECT sequences_cds.id, sequences_cds.sequence
FROM orthogrups
INNER JOIN sequences_cds ON orthogrups.id_protein = sequences_cds.id
'''

cursor.execute(cds_consulta)
cds_results = cursor.fetchall()

cds_records = []

#SeqRecord para as sequencias de CDS
for result in cds_results:
    id_protein, sequence = result
    record = SeqRecord(Seq(sequence), id=str(id_protein), description=str(id_cds))
    cds_records.append(record)

#Escrever as sequencias nos arquivos 
with open(cds_file, 'w') as cds_fasta:
    countSeq = 0
    for record in cds_records:
        SeqIO.write(cds_records, cds_fasta, 'fasta')
        countSeq += 1
        if countSeq % minSeq4Commit == 0:
         con.commit()


con.commit()
con.close()