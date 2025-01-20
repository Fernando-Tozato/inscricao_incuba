import csv
import os
import django
from datetime import datetime

# Configuração do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'incubadora.settings')
django.setup()

from database.models import Unidade, Controle

# Caminho para o arquivo CSV
csv_file_path_unidades = 'unidades.csv'
csv_file_path_controle = 'controle.csv'


# Função para importar os dados
def import_unidades_from_csv(csv_file_path):
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            nome = row['nome']
            endereco1 = row['endereco1']
            endereco2 = row['endereco2']

            unidade = Unidade(
                nome=nome,
                endereco1=endereco1,
                endereco2=endereco2,
            )

            # Salve a instância no banco de dados
            unidade.save()


def import_controle_from_csv(csv_file_path):
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        row = next(reader)

        inscricao_inicio = datetime.strptime(row['inscricao_inicio'] + ' -0300', '%d/%m/%Y %H:%M:%S %z')
        inscricao_fim = datetime.strptime(row['inscricao_fim'] + ' -0300', '%d/%m/%Y %H:%M:%S %z')
        sorteio_data = datetime.strptime(row['sorteio_data'] + ' -0300', '%d/%m/%Y %H:%M:%S %z')
        matricula_sorte_inicio = datetime.strptime(row['matricula_sorte_inicio'] + ' -0300', '%d/%m/%Y %H:%M:%S %z')
        matricula_sorte_fim = datetime.strptime(row['matricula_sorte_fim'] + ' -0300', '%d/%m/%Y %H:%M:%S %z')
        matricula_reman_inicio = datetime.strptime(row['matricula_reman_inicio'] + ' -0300', '%d/%m/%Y %H:%M:%S %z')
        matricula_reman_fim = datetime.strptime(row['matricula_reman_fim'] + ' -0300', '%d/%m/%Y %H:%M:%S %z')
        aulas_inicio = datetime.strptime(row['aulas_inicio'] + ' -0300', '%d/%m/%Y %H:%M:%S %z')
        aulas_fim = datetime.strptime(row['aulas_fim'] + ' -0300', '%d/%m/%Y %H:%M:%S %z')

        # Crie uma nova instância de Turma
        controle = Controle(
            inscricao_inicio=inscricao_inicio,
            inscricao_fim=inscricao_fim,
            sorteio_data=sorteio_data,
            matricula_sorte_inicio=matricula_sorte_inicio,
            matricula_sorte_fim=matricula_sorte_fim,
            matricula_reman_inicio=matricula_reman_inicio,
            matricula_reman_fim=matricula_reman_fim,
            aulas_inicio=aulas_inicio,
            aulas_fim=aulas_fim
        )

        # Salve a instância no banco de dados
        controle.save()


# Chame a função para importar os dados
if __name__ == '__main__':
    Unidade.objects.all().delete()
    Controle.objects.all().delete()
    import_unidades_from_csv(csv_file_path_unidades)
    import_controle_from_csv(csv_file_path_controle)
