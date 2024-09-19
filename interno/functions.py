from django.db.models import Q
from django.utils import timezone

from database.models import *


def grupo_necessario(user):
    return user.groups.filter(Q(name='Coord_Ped') | Q(name='Admin')).exists()


def ja_matriculado(cpf):
    return Aluno.objects.filter(cpf=cpf).exists()


# def ajustar_colunas(ws):
#     for col in ws.columns:
#         max_length = 0
#         column = get_column_letter(col[0].column)  # Obtém a letra da coluna
#         for cell in col:
#             try:
#                 if len(str(cell.value)) > max_length:
#                     max_length = len(str(cell.value))
#             finally:
#                 continue
#         adjusted_width = (max_length + 2)
#         ws.column_dimensions[column].width = adjusted_width
#
#
# def gerar_planilhas(professor):
#     curso_arq = {
#         'Informática para Iniciantes e Melhor Idade': 'info_melhor_idade',
#         'Informática Básica': 'info_basica',
#         'Excel Intermediário': 'excel_int',
#         'Excel Avançado': 'excel_ava',
#         'Montagem e Manutenção de Computadores': 'montagem',
#         'Robótica e Automação: Módulo 01': 'robotica_01',
#         'Robótica e Automação: Módulo 02': 'robotica_02',
#         'Robótica e Automação: Módulo 03': 'robotica_03',
#         'Design e Modelagem 3D: Módulo 01': 'design_01',
#         'Design e Modelagem 3D: Módulo 02': 'design_02',
#         'Gestão de Pessoas': 'gestao',
#         'Educação Financeira': 'educ_finan',
#         'Marketing Digital e Empreendedor': 'mark_digital_emp',
#         'Ferramentas do Marketing Digital': 'fer_mark_digital'
#     }
#
#     cursos = Turma.objects.filter(professor=professor).values_list('curso', flat=True).distinct()
#
#     for curso in cursos:
#         if not curso:
#             del cursos[cursos.index(curso)]
#             continue
#
#         wb = Workbook()
#         ws_presenca = wb.create_sheet(title='Presença')
#         ws_alunos = wb.create_sheet(title='Alunos')
#
#         ws_presenca = Presenca(ws_presenca, professor, curso).generate()
#
#         ajustar_colunas(ws_presenca)
#
#         ws_alunos = Alunos(ws_alunos, curso, professor).generate()
#
#         ajustar_colunas(ws_alunos)
#
#         filename = f'media/planilhas/presenca_{professor}_{curso_arq[curso]}.xlsx'
#         wb.save(filename)
#
#
# def criar_threads():
#     professores = Turma.objects.values_list('professor', flat=True).distinct()
#
#     threads = []
#
#     for professor in professores:
#         thread = threading.Thread(target=gerar_planilhas, args=(professor,))
#         threads.append(thread)
#
#     for thread in threads:
#         thread.start()
#
#     for thread in threads:
#         thread.join()


def verificar_inscritos(request, inscritos):
    if len(inscritos) == 0:
        return {'erro': 'Nenhum inscrito encontrado.'}

    inscritos = inscritos.exclude(cpf__in=Aluno.objects.values_list('cpf', flat=True))

    agora = timezone.now()
    controle = Controle.objects.first()
    matricula_sorteados = timezone.localtime(controle.matricula_sorteados)
    matricula_geral = timezone.localtime(controle.matricula_geral)
    matricula_fim = timezone.localtime(controle.matricula_fim)

    if agora < matricula_sorteados:
        return {'erro': 'O período de matrícula ainda não começou.'}

    if matricula_sorteados <= agora < matricula_geral:
        return inscritos.filter(ja_sorteado=True)

    if agora > matricula_fim:
        if grupo_necessario(request.user):
            return inscritos
        else:
            return {'erro': 'O período de matrícula já terminou.'}

    return inscritos


def matricula_valida(request, inscrito, turma):
    print(turma.num_alunos, turma.vagas)
    if turma.num_alunos >= turma.vagas:
        return False
    return True
