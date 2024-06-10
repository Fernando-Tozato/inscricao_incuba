import sqlite3

con = sqlite3.Connection('db.sqlite3')
cursor = con.cursor()

comandos = []
comandos.append('''
    DROP TABLE sqlite_sequence;
''')



for comando in comandos:
    cursor.execute(comando)

cursor.close()
con.close()