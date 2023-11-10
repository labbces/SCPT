from Bio import SeqIO 
import sqlite3 
from BioSQL import BioSeqDatabase

#minSeq4Commit
minSeq4Commit = 1000

#Variavel do arquivo FASTA 
fasta_file = "~/Dowloads/seq.fas"

# Variavel do banco de dados  

db_file = "mybiosql.db"

# Criando conexão com o banco de dados e um cursor  

server = BioSeqDatabase.open_database(driver = 'sqlite3', db = db_file) 

#print(server.keys())
db = server.new_database("sugarcane")
server.commit()
server.close()


#con = sqlite3.connect(db_file)
#cursor = con.cursor()

# Cria tabela "sequences" no banco de dados 

# cursor.execute("CREATE TABLE sequences (id, sequence)")

# # Define uma função para inserir sequências no banco de dados

# def insert_sequence(id, sequence):
#         cursor.execute("INSERT INTO sequence (id,sequence) VALUES (?, ?)", (id, sequence))

# #Lendo e inserindo sequências do arquivo FASTA no banco de dados

# #contador de sequencias 
# countSeq =  0

# for record in seqIO.parse(fasta_file, "fasta"):
#         countSeq += 1 
#         if countSeq % minSeq4Commit ==0:
#                 con.commit()
#         seq_id = record.id  # Obtém o ID da sequência 
#         seq_sequence = record.seq  # Obtém a sequência
#         insert_sequence(seq_id, seq_sequence) # Insere a sequência no banco de dados

# con.commit()  # Confirma alteração 
# con.close() # Fechar conexão com banco