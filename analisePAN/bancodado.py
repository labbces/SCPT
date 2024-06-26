import csv
from Bio import SeqIO 
import sqlite3 
from BioSQL import BioSeqDatabase

#Commit
minSeq4Commit = 1000

#Variavel dos arquivos
seq_CDS = "=/Storage/data1/jorge.munoz/FILES_PANTRANSCRIPTOME/all_CDS_idsok.fasta"
seq_OP = "/Storage/data1/jorge.munoz/FILES_PANTRANSCRIPTOME/PanTranscriptome_2023.proteins"
orthogrups_tvs = "/Storage/data1/jorge.munoz/FILES_PANTRANSCRIPTOME/Orthogroups_panTABLE.tsv"
# seq_CDS ="/home/hppp123/IC/teste/CDS.teste.fasta"
# seq_OP ="/home/hppp123/IC/teste/proteinas.teste.fasta"
# orthogrups_tvs ="/home/hppp123/IC/teste/orthogrupo.teste.fasta"

# Variavel do banco de dados  

db_file = "mybiosql.db"

#Criação da conexão com o banco de dados e do cursor 
con = sqlite3.connect(db_file)
cursor = con.cursor()

#TABELA CDS
cursor.execute("""
    CREATE TABLE IF NOT EXISTS sequences_CDS 
        (id VARCHAR(255), sequence TEXT)
""")

#TABELA proteinas 
cursor.execute("""
        CREATE TABLE IF NOT EXISTS sequences_protein
        (id VARCHAR(255), sequence TEXT)
""")

#TABELA orthogruops 
cursor.execute("""
        CREATE TABLE IF NOT EXISTS orthogrups
        (orthogroup VARCHAR(255), id_protein VARCHAR(255))
""")

# Define uma função para inserir sequências no banco de dados
def insert_sequence(cursor, table_name, seq_id, seq_sequence):
    cursor.execute("INSERT INTO {} (id, sequence) VALUES (?, ?)".format(table_name), (seq_id, seq_sequence))

#contador de sequencias 
countSeq  =  0

#Função para procesas o arquivo TSV e inserir no banco 
with open(orthogrups_tvs, 'r') as file:
        countSeq = 0 
        tvs_reader = csv.reader(file, delimiter='\t')
        for line in tvs_reader:
                countSeq +=1
                if countSeq % minSeq4Commit ==0: 
                        con.commit()
                orthogroup, id_protein = line  
                if orthogroup.startswith('Orthologue Group ID'):
                        continue 
                cursor.execute("INSERT INTO orthogrups (orthogroup, id_protein) VALUES (?, ?)", (orthogroup, id_protein))

 
#Lendo e inserindo sequências do arquivo CDS 
for record in SeqIO.parse(seq_CDS, "fasta"):
        countSeq += 1 
        if countSeq % minSeq4Commit ==0:
                con.commit()
        seq_id = record.id# Obtém o ID da sequência 
        seq_sequence = str(record.seq)  # Obtém a sequência
        insert_sequence(cursor, "sequences_CDS", seq_id, seq_sequence) # Insere a sequência no banco de dados
        



#Lendo e inserindo sequências do arquivo de proteínas 
#with gzip.open(seq_OP, "rt") as file:
with open(seq_OP, "r") as file:
    for record in SeqIO.parse(file, "fasta"):
        countSeq += 1 
        if countSeq % minSeq4Commit == 0:
            con.commit()
        seq_id = record.id  # Obtém o ID da sequência 
        seq_sequence = str(record.seq)  # Obtém a sequência
        insert_sequence(cursor, "sequences_protein", seq_id, seq_sequence) # Insere a sequência no banco de dados

        



con.commit()  # Confirma alteração 
con.close() # Fechar conexão com banco