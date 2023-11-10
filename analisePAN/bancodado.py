from Bio import SeqIo 
import sqlite3 

#Variavel do arquivo FASTA 
fasta_file = "all_transcripts_idsok.fasta"

# Variavel do banco de dados  

db_file = "bancosqlite.db"

# Criando conexão com o banco de dados e um cursor  

con = sqlite3.connect(db_file)
cursor = con.cursor()

# Cria tabela "sequences" no banco de dados 

cur.execute("CREATE TABLE sequences (id, sequence)")

# Define uma função para inserir sequências no banco de dados

def insert_sequence(id, sequence):
        cursor.execute("INSERT INTO sequence (id,sequence) VALUES (?, ?)", (id, sequence))

#Lendo e inserindo sequências do arquivo FASTA no banco de dados

for record in seqIO.parse(fasta_file, "fasta"):
        seq_id = record.id  # Obtém o ID da sequência 
        seq_sequence = record.seq  # Obtém a sequência
        insert_sequence(seq_id, seq_sequence) # Insere a sequência no banco de dados

con.commit()  # Confirma alteração 
con.close() # Fechar conexão com banc