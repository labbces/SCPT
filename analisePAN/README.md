 # Analise do pan-transcriptoma da cana de açucar 

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



