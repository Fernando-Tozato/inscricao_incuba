from database.models import Aluno


def ja_matriculado(cpf):
    return Aluno.objects.filter(cpf=cpf).exists()
