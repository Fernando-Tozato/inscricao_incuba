import sqlite3 as sql
import pandas as pd
import os

if os.path.exists('alunos.xlsx'):
    os.remove('alunos.xlsx')

if os.path.exists('turmas.xlsx'):
    os.remove('turmas.xlsx')

conn = sql.connect('db.sqlite3')

query_alunos = 'SELECT * FROM core_aluno'
query_turmas = 'SELECT * FROM core_turma'

df_alunos = pd.read_sql_query(query_alunos, conn)
df_turmas = pd.read_sql_query(query_turmas, conn)

conn.close()

df_alunos.to_excel('alunos.xlsx', index=False)
df_turmas.to_excel('turmas.xlsx', index=False)