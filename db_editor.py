# sourcery skip: merge-list-append, merge-list-appends-into-extend, merge-list-extend
import sqlite3

con = sqlite3.Connection('db.sqlite3')
cursor = con.cursor()

comandos = []


comandos.append('''
    DROP TABLE auth_permission;
''')

comandos.append('''
    DROP TABLE auth_group;
''')

comandos.append('''
    DROP TABLE auth_user;
''')

comandos.append('''
    DROP TABLE django_session;
''')

for comando in comandos:
    cursor.execute(comando)

cursor.close()
con.close()