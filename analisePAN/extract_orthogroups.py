import sqlite3

db_file="mybiosql.db"
con=sqlite3(db_file)
cursor=con.cursor

orthogroup_query = '''
SELECT orthogroup
FROM orthogrups
GROUP BY orthogroup
HAVING COUNT(*) > 4
'''

cursor.execute(orthogroup_query)
orthogroup_results = cursor.fetchall()

output_file = "4moreOG.txt"

with open(output_file,"w") as f: 
    for row in orthogroup_results:
        f.write(row[0]+"/n")

con.close()