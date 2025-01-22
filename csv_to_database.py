import csv
import os
from datetime import datetime
from pathlib import Path
from typing import Any

import django

# Configuração do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'incubadora.settings')
django.setup()

from database.models import Unidade, Controle, Curso, Turma

csv_file_path_controle = Path('controle.csv')
csv_file_path_unidades = Path('unidades.csv')
csv_file_path_curso = Path('cursos.csv')
csv_file_path_turmas = Path('turmas.csv')

def csv_to_dict(csv_file_path: Path) -> list[dict[str | Any, str | Any]]:
    with open(csv_file_path, encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        return list(reader)

def dict_to_database(data: list, model):
    objects = []

    for line in data:
        if "horario_entrada" in line:
            line["horario_entrada"] = datetime.strptime(line["horario_entrada"], "%H:%M").time()
        if "horario_saida" in line:
            line["horario_saida"] = datetime.strptime(line["horario_saida"], "%H:%M").time()

        m2m_data, m2m_field = None, None

        if 'unidade' in line:
            m2m_field = 'unidades'
            m2m_data = line.pop(m2m_field, '')

        obj = model.objects.create(**line)

        if m2m_data == '':
            ids = input(f"Digite os IDs para '{m2m_field}' do objeto '{obj}': ")
            ids_list = [int(i) for i in ids.split(',') if i.strip().isdigit()]

            if ids_list:
                obj.unidades.set(ids_list)
        elif m2m_data is not None:
            obj.unidades.set(m2m_data)

        objects.append(obj)

    model.objects.bulk_create(objects)
    print(f'{len(objects)} registrados no banco de dados com sucesso!')


def main():
    if csv_file_path_controle.exists():
        if Controle.objects.first() is None:
            controle_list: list = csv_to_dict(csv_file_path_controle)
            dict_to_database(controle_list, Controle)

    if csv_file_path_unidades.exists():
        if Unidade.objects.first() is None:
            unidades_list: list = csv_to_dict(csv_file_path_unidades)
            dict_to_database(unidades_list, Unidade)

    if csv_file_path_curso.exists():
        if Curso.objects.first() is None:
            curso_list: list = csv_to_dict(csv_file_path_curso)
            dict_to_database(curso_list, Curso)

    if csv_file_path_turmas.exists():
        if Turma.objects.first() is None:
            turmas_list: list = csv_to_dict(csv_file_path_turmas)
            dict_to_database(turmas_list, Turma)


if __name__ == '__main__':
    main()