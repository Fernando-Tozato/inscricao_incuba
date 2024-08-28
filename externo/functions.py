import datetime
import hashlib
import json
import re
import uuid

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import QuerySet

from database.models import Turma, Inscrito


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


def gerar_hash(dado: str, salt: str) -> str:
    dado_com_salt: str = dado + salt
    codigo_hash: str = hashlib.sha256(dado_com_salt.encode()).hexdigest()
    numero_inteiro = int(codigo_hash, 16)
    return f'{(numero_inteiro % 10000):04d}'


def gerar_numero_inscricao(nome: str, cpf: str, nascimento: str) -> str:
    salt: str = uuid.uuid4().hex

    hash_nome: str = gerar_hash(nome, salt)
    hash_cpf: str = gerar_hash(cpf, salt)
    hash_nascimento: str = gerar_hash(nascimento, salt)

    return f'{hash_nome}.{hash_cpf}.{hash_nascimento}'
