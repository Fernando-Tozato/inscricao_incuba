# sourcery skip: merge-list-append, merge-list-appends-into-extend, merge-list-extend
import sqlite3

con = sqlite3.Connection('db.sqlite3')
cursor = con.cursor()

comandos = []

comandos.append('''
    DROP TABLE auth_group;
''')

comandos.append('''
    DROP TABLE auth_group_permissions;
''')

comandos.append('''
    DROP TABLE auth_permission;
''')

comandos.append('''
    DROP TABLE auth_user;
''')

comandos.append('''
    DROP TABLE auth_user_groups;
''')

comandos.append('''
    DROP TABLE auth_user_user_permissions;
''')

comandos.append('''
    DROP TABLE database_aluno;
''')

comandos.append('''
    DROP TABLE database_controle;
''')

comandos.append('''
    DROP TABLE database_inscrito;
''')

comandos.append('''
    DROP TABLE database_turma;
''')

comandos.append('''
    DROP TABLE django_admin_log;
''')

comandos.append('''
    DROP TABLE django_content_type;
''')

comandos.append('''
    DROP TABLE django_migrations;
''')

comandos.append('''
    DROP TABLE django_session;
''')



for comando in comandos:
    cursor.execute(comando)

cursor.close()
con.close()