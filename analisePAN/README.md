 # Analise do pan-transcriptoma da cana de açucar 

 Este projeto visa importar sequências de CDS e proteínas de arquivos FASTA, além de importar dados de grupos ortológicos de um arquivo TSV para um banco de dados SQLite, e posteriormente extrair essas sequências para arquivos FASTA individuais para análise adicional.



 ## Extrair as sequencias dos grupos ortologos 

 Descarregar o esquema do BioSQL

 ```
 wget https://raw.githubusercontent.com/biosql/biosql/master/sql/biosqldb-sqlite.sql 
 ```

 instalar o Sqlite3
 
 ```
 sudo apt install sqlite3
 ```

 Iniciar o banco sqlite com o BioSQL
 
```
sqlite3 bancosqlite.db < biosqldb-sqlite.sql 
```

# Scripts 

## Script 1: bancodado.py
Este primeiro script tem a finalidade de criar um banco de dados SQLite, definir tabelas e inserir dados provenientes de arquivos de proteinas, CDS e grupos ortológos. 

 ## Requisitos 

 - SQLite3
- Bibliotecas Python:
    * Biopython (para manipulação de sequências biológicas)
    * sqlite3 (para interação com o banco de dados SQLite)

## Execução do Script
1. Criação do banco de dados e tabelas:
* O script começa conectando-se com um banco de dado SQLite chamado "mybiosql.db" 
* Crianção de três tabelas no banco de dados: "sequence_CDS", "sequences_protein" e "orthogrups". 

2. Inserindo as sequencias na tabela:
* A função ``insert_sequence`` é responsavel por inserir sequências nas tabelas do banco de dados. 

3. Leitura das sequencias dos arquivos FASTA:
* Uso da biblioteca SeqIO para analisar os arquivos de sequencias com a função  `` Bio.SeqIO.parce()``

4. Função ``process_tvs``: 
* Arquivos em formato TSV não são processados pela biblioteca SeqIO, então usei a biblioteca CSV para lidar com esse arquivo. 
* Criação de uma função para lidar com a leitura do arquivo tvs e ser inserido no banco de dados. 

5. Controle de commit e encerramento do banco. 
* A cada leitura ou inserção, o script verifica se um número específico de sequências (`minSeq4Commit`) foi atingido e realiza um commit no banco de dados. 
* No final, após todas as operações, é realizado um commit final e a conexão com banco de dados é fechada. 


## Script 2: extração.py 
Este script extrai sequências de CDS e proteínas dos grupos ortológicos que possuem mais de três sequências, e grava essas sequências em arquivos FASTA individuais.

## Requisitos 
* BioSQL (para conectar ao banco de dados BioSQL)
- Bibliotecas Python:

    * Biopython (para manipulação de sequências biológicas)
    * sqlite3 (para interação com o banco de dados SQLite)

## Execução do Script 

1. Conexão com o banco de dados:
* O script se conecta ao banco de dados SQLite especificado `mybiosql.db`.
2. Consulta ao banco de dados: 
* O script executa duas consultas:
    * `count_selected_orthogroups_query`: Conta o número de grupos de ortólogos que têm mais de 3 sequências.
    * `orthogroup_consulta`: Recupera os IDs dos grupos de ortólogos que têm mais de 3 sequências.
3. Processamento de Cada Grupo de Ortólogos
* Para cada grupo de ortólogos encontrado na consulta anterior, o script extrai as sequências de proteínas e CDS associadas e então são armazenadas em adquivos FASTA separados.
4. Finalização
* Após todas as operações, é realizado um commit final e a conexão com banco de dados é fechada.