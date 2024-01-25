from BioSQL import BioSeqDatabase
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import sqlite3
from Bio.Seq import Seq

  
db_file = "mybiosql.db"
protein_file = "/home/hppp123/IC/orto_protein.fas"
cds_file = "/home/hppp123/IC/orto_CDS.fas"

minSeq4Commit = 10



con = sqlite3.connect(db_file)
cursor = con.cursor()


protein_consulta = '''
SELECT orthogrups.id_protein , sequences_protein.id
FROM orthogrups
INNER JOIN sequences_protein ON orthogrups.id_protein = sequences_protein.id
'''

cursor.execute(protein_consulta)
protein_results = cursor.fetchall()


cds_consulta = '''
SELECT orthogrups.id_protein , sequences_cds.id
FROM orthogrups
INNER JOIN sequences_cds ON orthogrups.id_protein = sequences_cds.id
'''

cursor.execute(cds_consulta)
cds_results = cursor.fetchall()


protein_records = []
for result in protein_results:
    id_protein, sequence = result
    record = SeqRecord(Seq(sequence), id=str(id_protein))
    protein_records.append(record)


with open(protein_file, 'w') as protein_fasta:
    countSeq = 0
    SeqIO.write(protein_records, protein_fasta, 'fasta')
    countSeq += 1
    if countSeq % minSeq4Commit  == 0:
        con.commit()




cds_records = []
for result in cds_results:
    id_protein, sequence = result
    record = SeqRecord(Seq(sequence), id=str(id_protein))
    cds_records.append(record)

with open(cds_file, 'w') as cds_fasta:
    countSeq = 0
    SeqIO.write(cds_records, cds_fasta, 'fasta')
    countSeq += 1
    if countSeq % minSeq4Commit == 0:
        con.commit()


con.commit()
con.close()