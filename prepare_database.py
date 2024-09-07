import csv
import os
import django
from datetime import datetime

# Configuração do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'incubadora.settings')
django.setup()

from database.models import Turma, Controle

# Caminho para o arquivo CSV
csv_file_path_turmas = 'turmas.csv'
csv_file_path_controle = 'controle.csv'


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


def import_controle_from_csv(csv_file_path):
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        row = next(reader)

        inscricao_inicio = datetime.strptime(row['inscricao_inicio'] + ' -0300', '%d/%m/%Y %H:%M:%S %z')
        inscricao_fim = datetime.strptime(row['inscricao_fim'] + ' -0300', '%d/%m/%Y %H:%M:%S %z')
        sorteio_data = datetime.strptime(row['sorteio_data'] + ' -0300', '%d/%m/%Y %H:%M:%S %z')
        matricula_sorteados = datetime.strptime(row['matricula_sorteados'] + ' -0300', '%d/%m/%Y %H:%M:%S %z')
        vagas_disponiveis = datetime.strptime(row['vagas_disponiveis'] + ' -0300', '%d/%m/%Y %H:%M:%S %z')
        matricula_geral = datetime.strptime(row['matricula_geral'] + ' -0300', '%d/%m/%Y %H:%M:%S %z')
        matricula_fim = datetime.strptime(row['matricula_fim'] + ' -0300', '%d/%m/%Y %H:%M:%S %z')
        aulas_inicio = datetime.strptime(row['aulas_inicio'] + ' -0300', '%d/%m/%Y %H:%M:%S %z')
        aulas_fim = datetime.strptime(row['aulas_fim'] + ' -0300', '%d/%m/%Y %H:%M:%S %z')

        # Crie uma nova instância de Turma
        controle = Controle(
            inscricao_inicio=inscricao_inicio,
            inscricao_fim=inscricao_fim,
            sorteio_data=sorteio_data,
            matricula_sorteados=matricula_sorteados,
            vagas_disponiveis=vagas_disponiveis,
            matricula_geral=matricula_geral,
            matricula_fim=matricula_fim,
            aulas_inicio=aulas_inicio,
            aulas_fim=aulas_fim
        )

        # Salve a instância no banco de dados
        controle.save()


# Chame a função para importar os dados
if __name__ == '__main__':
    Turma.objects.all().delete()
    Controle.objects.all().delete()
    import_turmas_from_csv(csv_file_path_turmas)
    import_controle_from_csv(csv_file_path_controle)
