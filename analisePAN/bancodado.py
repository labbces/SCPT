from Bio import SeqIO 
import sqlite3 
from BioSQL import BioSeqDatabase

#minSeq4Commit
minSeq4Commit = 1000

#Variavel do arquivo FASTA 
fasta_file = "/home/hppp123/IC/SCPT/analisePAN/seq.fas"

# Variavel do banco de dados  

db_file = "mybiosql.db"

#Criação da conexão com o banco de dados e do cursor 
con = sqlite3.connect(db_file)
cursor = con.cursor()

#criar tabela 
cursor.execute("""
    CREATE TABLE IF NOT EXISTS sequences 
        (id VARCHAR(255), sequence TEXT)
""")


# Define uma função para inserir sequências no banco de dados

def insert_sequence(cursor, seq_id, seq_sequence):
        seq_sequence_str = str(seq_sequence)
        cursor.execute("INSERT INTO sequences (id,sequence) VALUES (?, ?)", (seq_id, seq_sequence_str))

#contador de sequencias 
countSeq =  0

#Lendo e inserindo sequências do arquivo FASTA no banco de dados

for record in SeqIO.parse(fasta_file, "fasta"):
        countSeq += 1 
        if countSeq % minSeq4Commit ==0:
                con.commit()
        seq_id = record.id  # Obtém o ID da sequência 
        seq_sequence = record.seq  # Obtém a sequência
        insert_sequence(cursor, seq_id, seq_sequence) # Insere a sequência no banco de dados

con.commit()  # Confirma alteração 
con.close() # Fechar conexão com banco