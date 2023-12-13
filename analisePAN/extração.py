from BioSQL import BioSeqDatabase

#Conexão com o banco de dados 
server = BioSeqDatabase.open_database(
    driver="mysql.connector",
    host= "/home/hppp123/IC/SCPT/analisePAN/bancodado.py",
    db= "mybiosql.db"
)

# Variaveis para as tabelas (namespaces)
protein_db = server["sequences_protein"]
orthogrups_db = server["orthogrups"]
CDS_db = server["sequences_CDS"]

#Percorres os identificadores do ortogrups 
for xxx in ["xxx"]:
    seq_recors = db.lookup
