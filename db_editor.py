# sourcery skip: merge-list-append, merge-list-appends-into-extend, merge-list-extend
import sqlite3

con = sqlite3.Connection('db.sqlite3')
cursor = con.cursor()

comandos = ['''
    DROP TABLE auth_group;
''', '''
    DROP TABLE auth_group_permissions;
''', '''
    DROP TABLE auth_permission;
''', '''
    DROP TABLE auth_user;
''', '''
    DROP TABLE auth_user_groups;
''', '''
    DROP TABLE auth_user_user_permissions;
''', '''
    DROP TABLE database_aluno;
''', '''
    DROP TABLE database_controle;
''', '''
    DROP TABLE database_inscrito;
''', '''
    DROP TABLE database_turma;
''', '''
    DROP TABLE django_admin_log;
''', '''
    DROP TABLE django_content_type;
''', '''
    DROP TABLE django_migrations;
''', '''
    DROP TABLE django_session;
''']

for comando in comandos:
    cursor.execute(comando)

cursor.close()
con.close()
