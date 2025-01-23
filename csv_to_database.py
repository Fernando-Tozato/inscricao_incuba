import csv
import os
from datetime import datetime
from pathlib import Path
from typing import Any
import pandas as pd

import django

# Configuração do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'incubadora.settings')
django.setup()

from database.models import Unidade, Controle, Curso, Turma

csv_file_path_controle = Path('controle.csv')
csv_file_path_unidades = Path('unidades.csv')
csv_file_path_curso = Path('cursos.csv')
csv_file_path_turmas = Path('turmas.csv')

def csv_to_list(csv_file_path: Path) -> list[dict[str | Any, str | Any]]:
    with open(csv_file_path, encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        return list(reader)

def csv_to_controle():
    df = pd.read_csv(csv_file_path_controle)

    for coluna in df.columns:
        df[coluna] = pd.to_datetime(df[coluna], format='%Y-%m-%d %H:%M:%S', utc=True)
        df[coluna] = df[coluna].dt.tz_convert('America/Sao_Paulo')

    data = df.to_dict(orient='records')

    Controle.objects.create(**data[0])

def list_to_database(data, model):
    objects = []
    for line in data:
        if 'horario_entrada' in line:
            line['horario_entrada'] = datetime.strptime(line['horario_entrada'], '%H:%M').time()
        if 'horario_saida' in line:
            line['horario_saida'] = datetime.strptime(line['horario_saida'], '%H:%M').time()
        obj = model.objects.create(**line)
        objects.append(obj)
    model.objects.bulk_create(objects)

def list_to_curso(data):
    objects = []

    for line in data:
        m2m_field = 'unidades'
        m2m_value = line.pop(m2m_field)

        if ',' in m2m_value:
            m2m_value = tuple(m2m_value.split(','))

        obj = Curso.objects.create(**line)
        obj.unidades.add(*m2m_value)

        objects.append(obj)
    Curso.objects.bulk_create(objects)




def main():
    if csv_file_path_controle.exists() and Controle.objects.first() is None:
        try:
            csv_to_controle()
        except:
            pass

    if csv_file_path_unidades.exists() and Unidade.objects.first() is None:
        try:
            unidades_list: list = csv_to_list(csv_file_path_unidades)
            list_to_database(unidades_list, Unidade)
        except:
            pass

    if csv_file_path_curso.exists() and Curso.objects.first() is None:
        try:
            curso_list: list = csv_to_list(csv_file_path_curso)
            list_to_curso(curso_list)
        except:
            pass

    if csv_file_path_turmas.exists() and Turma.objects.first() is None:
        try:
            turmas_list: list = csv_to_list(csv_file_path_turmas)
            list_to_database(turmas_list, Turma)
        except:
            pass


if __name__ == '__main__':
    main()