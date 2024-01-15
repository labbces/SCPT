import csv
from Bio import SeqIO 
import sqlite3 
from BioSQL import BioSeqDatabase

#minSeq4Commit
minSeq4Commit = 10
#Variavel dos arquivos
sequences_CDS = "/home/hppp123/IC/SCPT/analisePAN/testes.fasta/CDS.teste.fasta"
sequences_protein = "/home/hppp123/IC/SCPT/analisePAN/testes.fasta/protein_teste.fasta"
orthogrups_tvs = "/home/hppp123/IC/SCPT/analisePAN/testes.fasta/teste.orthogrupo"



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
        (id_grupo VARCHAR(255), id_protein VARCHAR(255))
""")

# Define uma função para inserir sequências no banco de dados

def insert_sequence(cursor, table_name, seq_id, seq_sequence):
        seq_sequence_str = str(seq_sequence)
        cursor.execute("INSERT INTO {} (id, sequence) VALUES (?, ?)".format(table_name), (seq_id, seq_sequence_str))

#contador de sequencias 
countSeq =  0

# Função para procesas o arquivo TSV e inserir no banco 

with open(orthogrups_tvs, 'r') as file:
        countSeq = 0 
        tvs_reader = csv.reader(file, delimiter='\t')
        for line in tvs_reader:
                countSeq +=1
                if countSeq % minSeq4Commit ==0: 
                        con.commit()
                id_grupo, id_protein = line  
                if id_grupo.startswith('Orthologue Group ID'):
                        continue 
                cursor.execute("INSERT INTO orthogrups (id_grupo, id_protein) VALUES (?, ?)", (id_grupo, id_protein))


#Lendo e inserindo sequências do arquivo CDS 
for record in SeqIO.parse(sequences_CDS, "fasta"):
        countSeq += 1 
        if countSeq % minSeq4Commit ==0:
                con.commit()
        seq_id = record.id  # Obtém o ID da sequência 
        seq_sequence = record.seq  # Obtém a sequência
        insert_sequence(cursor, "sequences_CDS", seq_id, seq_sequence) # Insere a sequência no banco de dados

#Lendo e inserindo sequências do arquivo de proteínas 
for record in SeqIO.parse(sequences_protein, "fasta"):
        countSeq += 1 
        if countSeq % minSeq4Commit ==0:
                con.commit()
        seq_id = record.id  # Obtém o ID da sequência 
        seq_sequence = record.seq  # Obtém a sequência
        insert_sequence(cursor, "sequences_protein", seq_id, seq_sequence) # Insere a sequência no banco de dados

con.commit()  # Confirma alteração 
con.close() # Fechar conexão com banco