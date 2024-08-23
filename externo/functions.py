import json
import datetime

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import QuerySet

from database.models import Turma


def get_turmas_as_json(campos: list[str] | None = None) -> str:
    turmas: QuerySet[Turma] = Turma.objects.all()
    turmas_list: list[dict] = []

    if campos is None:
        campos = [
            'curso', 'dias', 'horario_entrada', 'horario_saida', 'vagas',
            'escolaridade', 'idade', 'professor', 'num_alunos',
            'horario', 'cotas', 'ampla_conc'
        ]

    for turma in turmas:
        turma_dict: dict[str: str | int] = {}

        for campo in campos:
            if hasattr(turma, campo):
                valor = getattr(turma, campo)
                if callable(valor):  # Se o atributo for um método, chama-o
                    valor = valor()
                if isinstance(valor, datetime.time | datetime.datetime):
                    valor = valor.strftime("%H:%M")  # Formatação para campos de horário
                turma_dict[campo] = valor

        turmas_list.append(turma_dict)

    return json.dumps(turmas_list, cls=DjangoJSONEncoder)
