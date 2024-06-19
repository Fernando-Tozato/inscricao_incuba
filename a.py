import sqlite3
import csv

# Nome do banco de dados SQLite e do arquivo CSV
db_name = 'db.sqlite'
csv_file = 'turmas.csv'

# Conecta ao banco de dados (ou cria se não existir)
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Cria a tabela (ajuste os tipos de dados conforme necessário)
cursor.execute('''
CREATE TABLE IF NOT EXISTS minha_tabela (
    coluna1 TEXT,
    coluna2 INTEGER,
    coluna3 REAL
)
''')

# Lê o arquivo CSV e insere os dados na tabela
with open(csv_file, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    # Pula o cabeçalho do CSV
    next(reader)
    # Insere cada linha do CSV na tabela
    for row in reader:
        cursor.execute('''
        INSERT INTO minha_tabela (coluna1, coluna2, coluna3)
        VALUES (?, ?, ?)
        ''', row)

# Salva (commit) as mudanças e fecha a conexão
conn.commit()
conn.close()
