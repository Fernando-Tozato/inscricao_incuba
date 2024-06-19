import csv
import os
import django
from datetime import datetime

# Configuração do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'incubadora.settings')
django.setup()

from database.models import Turma

# Caminho para o arquivo CSV
csv_file_path = 'turmas.csv'

# Função para importar os dados
def import_turmas_from_csv(csv_file_path):
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            curso = row['curso']
            dias = row['dias']
            horario_entrada = datetime.strptime(row['horario_entrada'], '%H:%M').time()
            horario_saida = datetime.strptime(row['horario_saida'], '%H:%M').time()
            vagas = int(row['vagas'])
            escolaridade = int(row['escolaridade'])
            idade = int(row['idade'])
            professor = row['professor']

            # Crie uma nova instância de Turma
            turma = Turma(
                curso=curso,
                dias=dias,
                horario_entrada=horario_entrada,
                horario_saida=horario_saida,
                vagas=vagas,
                escolaridade=escolaridade,
                idade=idade,
                professor=professor
            )

            # Salve a instância no banco de dados
            turma.save()

# Chame a função para importar os dados
import_turmas_from_csv(csv_file_path)
