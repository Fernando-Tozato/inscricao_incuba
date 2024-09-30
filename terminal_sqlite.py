import sqlite3
import pandas as pd


# Função para criar a conexão com o banco de dados
def connect_db(db_name="db.sqlite3"):
    conn = sqlite3.connect(db_name)
    return conn


# Função para executar comandos SQL e retornar resultados
def execute_sql(conn, sql_command):
    try:
        cursor = conn.cursor()
        cursor.execute(sql_command)

        if sql_command.strip().lower().startswith("select"):
            df = pd.read_sql_query(sql_command, conn)
            print(df)
        else:
            conn.commit()
            print("Comando executado com sucesso.")
    except Exception as e:
        print(f"Erro ao executar comando: {e}")


# Função para exibir o terminal interativo
def terminal():
    conn = connect_db()

    while True:
        print("\nTerminal SQLite (Digite 'exit' para sair)")
        sql_command = input("sqlite> ")

        if sql_command.lower() == "exit":
            print("Saindo...")
            conn.close()
            break

        execute_sql(conn, sql_command)


# Executar o terminal
if __name__ == "__main__":
    terminal()
