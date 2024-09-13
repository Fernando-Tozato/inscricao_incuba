import logging
import random
from datetime import timedelta

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.db.models import Q
from django.db.models.functions import Coalesce
from django.template.loader import render_to_string
from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter

from database.models import *


def avisar_sorteados(request, emails, sorteado=False):
    controle = Controle.objects.first()

    subject = 'Incubadora de Robótica'

    if sorteado:
        email_template_name = "emails/aviso_sorteado.html"
        c = {
            'domain': get_current_site(request).domain,
            'protocol': 'http',
            'data_matricula_inicio': controle.matricula_sorteados,  # type: ignore
            'data_matricula_fim': controle.matricula_fim,  # type: ignore
            'data_aulas_inicio': controle.aulas_inicio,  # type: ignore
        }
        email_content = render_to_string(email_template_name, c)

    else:
        email_template_name = 'emails/aviso_nao_sorteado.html'
        c = {
            'domain': get_current_site(request).domain,
            'protocol': 'http',
            'data_matricula_inicio': controle.matricula_geral,  # type: ignore
            'data_matricula_fim': controle.matricula_fim,  # type: ignore
            'data_aulas_inicio': controle.aulas_inicio,  # type: ignore
        }
        email_content = render_to_string(email_template_name, c)


    email_message = EmailMultiAlternatives(subject, '', 'nao_responda@incubarobotica.com.br', emails)
    email_message.attach_alternative(email_content, "text/html")

    try:
        email_message.send()
        print('enviado')
    except Exception as e:
        print(e)

    print('Fim')




def ajustar_colunas(ws):
    for col in ws.columns:
        max_length = 0
        column = get_column_letter(col[0].column)  # Obtém a letra da coluna
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column].width = adjusted_width


def gerar_planilhas():
    aulas_inicio = Controle.objects.first().aulas_inicio  # type: ignore
    aulas_fim = Controle.objects.first().aulas_fim  # type: ignore

    curso_arq = {
        'Informática para Iniciantes e Melhor Idade': 'info_melhor_idade',
        'Informática Básica': 'info_basica',
        'Excel Intermediário': 'excel_int',
        'Excel Avançado': 'excel_ava',
        'Montagem e Manutenção de Computadores': 'montagem',
        'Robótica e Automação: Módulo 01': 'robotica_01',
        'Robótica e Automação: Módulo 02': 'robotica_02',
        'Robótica e Automação: Módulo 03': 'robotica_03',
        'Design e Modelagem 3D: Módulo 01': 'design_01',
        'Design e Modelagem 3D: Módulo 02': 'design_02',
        'Gestão de Pessoas': 'gestao',
        'Educação Financeira': 'educ_finan',
        'Marketing Digital e Empreendedor': 'mark_digital_emp',
        'Ferramentas do Marketing Digital': 'fer_mark_digital'
    }

    turmas = Turma.objects.all()
    professores = [turma.professor for turma in turmas]

    for professor in professores:
        cursos = [(turma.curso if turma.professor == professor else None) for turma in turmas]

        for curso in cursos:
            if not curso:
                del cursos[cursos.index(curso)]
                continue

            wb = Workbook()
            ws_presenca = wb.create_sheet(title='Presença')

            turmas_aux = Turma.objects.filter(Q(professor=professor) & Q(curso=curso))

            start_row = 1
            for turma in turmas_aux:
                sabados = []
                domingos = []

                # Título da Turma
                header = f'{turma.dias} {turma.horario()}'
                ws_presenca.merge_cells(start_row=start_row, start_column=1, end_row=start_row, end_column=2)
                ws_presenca.cell(row=start_row, column=1).value = header
                ws_presenca.cell(row=start_row, column=1).font = Font(bold=True)
                ws_presenca.cell(row=start_row, column=1).alignment = Alignment(horizontal="center")

                # LEGENDA
                # Presente
                ws_presenca.merge_cells(start_row=start_row, start_column=3, end_row=start_row, end_column=4)
                ws_presenca.cell(row=start_row, column=3).value = 'Presente'
                ws_presenca.cell(row=start_row, column=3).font = Font(bold=True)
                ws_presenca.cell(row=start_row, column=3).alignment = Alignment(horizontal="center")
                ws_presenca.cell(row=start_row, column=5).value = 'P'
                ws_presenca.cell(row=start_row, column=5).font = Font(bold=True)
                ws_presenca.cell(row=start_row, column=5).alignment = Alignment(horizontal="center")
                ws_presenca.cell(row=start_row, column=5).fill = PatternFill(start_color="6aa84f", end_color="6aa84f",
                                                                             fill_type="solid")

                # Faltoso
                ws_presenca.merge_cells(start_row=start_row, start_column=7, end_row=start_row, end_column=8)
                ws_presenca.cell(row=start_row, column=7).value = 'Faltoso'
                ws_presenca.cell(row=start_row, column=7).font = Font(bold=True)
                ws_presenca.cell(row=start_row, column=7).alignment = Alignment(horizontal="center")
                ws_presenca.cell(row=start_row, column=9).value = 'F'
                ws_presenca.cell(row=start_row, column=9).font = Font(bold=True)
                ws_presenca.cell(row=start_row, column=9).alignment = Alignment(horizontal="center")
                ws_presenca.cell(row=start_row, column=9).fill = PatternFill(start_color="cc0000", end_color="cc0000",
                                                                             fill_type="solid")

                # Fim de Semana
                ws_presenca.merge_cells(start_row=start_row, start_column=11, end_row=start_row, end_column=12)
                ws_presenca.cell(row=start_row, column=11).value = 'Fim de Semana'
                ws_presenca.cell(row=start_row, column=11).font = Font(bold=True)
                ws_presenca.cell(row=start_row, column=11).alignment = Alignment(horizontal="center")
                ws_presenca.cell(row=start_row, column=13).value = 'S/D'
                ws_presenca.cell(row=start_row, column=13).font = Font(bold=True)
                ws_presenca.cell(row=start_row, column=13).alignment = Alignment(horizontal="center")
                ws_presenca.cell(row=start_row, column=13).fill = PatternFill(start_color="3d85c6", end_color="3d85c6",
                                                                              fill_type="solid")

                # Feriado
                ws_presenca.merge_cells(start_row=start_row, start_column=15, end_row=start_row, end_column=16)
                ws_presenca.cell(row=start_row, column=15).value = 'Feriado'
                ws_presenca.cell(row=start_row, column=15).font = Font(bold=True)
                ws_presenca.cell(row=start_row, column=15).alignment = Alignment(horizontal="center")
                ws_presenca.cell(row=start_row, column=17).value = 'H'
                ws_presenca.cell(row=start_row, column=17).font = Font(bold=True)
                ws_presenca.cell(row=start_row, column=17).alignment = Alignment(horizontal="center")
                ws_presenca.cell(row=start_row, column=17).fill = PatternFill(start_color="f1c232", end_color="f1c232",
                                                                              fill_type="solid")

                # Títulos de coluna
                ws_presenca.cell(row=start_row + 1, column=1).value = 'ID'
                ws_presenca.cell(row=start_row + 1, column=2).value = 'Nome'

                for col in range(3, (aulas_fim - aulas_inicio).days + 4):
                    dia_aula = aulas_inicio + timedelta(days=col - 3)
                    ws_presenca.cell(row=start_row + 1, column=col).value = dia_aula.strftime('%d/%m')
                    if dia_aula.weekday() == 5:
                        sabados.append(col)
                    elif dia_aula.weekday() == 6:
                        domingos.append(col)

                for col in range(1, ws_presenca.max_column + 1):
                    cell = ws_presenca.cell(row=start_row + 1, column=col)
                    cell.font = Font(bold=True)
                    cell.alignment = Alignment(horizontal="center")

                # Alunos
                alunos = Aluno.objects.filter(id_turma=turma).annotate(
                    nome_ordenacao=Coalesce('nome_social', 'nome')).order_by('nome_ordenacao')

                idx = 0

                for idx, aluno in enumerate(alunos):
                    ws_presenca.cell(row=idx + start_row + 2, column=1).value = aluno.pk
                    ws_presenca.cell(row=idx + start_row + 2,
                                     column=2).value = aluno.nome_social if aluno.nome_social else aluno.nome
                    for col in sabados + domingos:
                        ws_presenca.cell(row=idx + start_row + 2, column=col).font = Font(bold=True)
                        ws_presenca.cell(row=idx + start_row + 2, column=col).alignment = Alignment(horizontal="center")
                        ws_presenca.cell(row=idx + start_row + 2, column=col).fill = PatternFill(start_color="3d85c6",
                                                                                                 end_color="3d85c6",
                                                                                                 fill_type="solid")
                        if col in sabados:
                            ws_presenca.cell(row=idx + start_row + 2, column=col).value = 'S'
                        else:
                            ws_presenca.cell(row=idx + start_row + 2, column=col).value = 'D'

                # Formatação Condicional
                range_str = f"C{start_row + 2}:{get_column_letter(ws_presenca.max_column)}{idx + start_row + 2}"
                red_fill = PatternFill(start_color="cc0000", end_color="cc0000", fill_type="solid")
                green_fill = PatternFill(start_color="6aa84f", end_color="6aa84f", fill_type="solid")
                yellow_fill = PatternFill(start_color="f1c232", end_color="f1c232", fill_type="solid")

                ws_presenca.conditional_formatting.add(range_str,
                                                       CellIsRule(operator='equal', formula=['"F"'], fill=red_fill))
                ws_presenca.conditional_formatting.add(range_str,
                                                       CellIsRule(operator='equal', formula=['"P"'], fill=green_fill))
                ws_presenca.conditional_formatting.add(range_str,
                                                       CellIsRule(operator='equal', formula=['"H"'], fill=yellow_fill))

                # Espaçamento
                max_row = idx + start_row + 3
                for col in range(1, ws_presenca.max_column + 1):
                    ws_presenca.cell(row=max_row, column=col).fill = PatternFill(start_color="000000",
                                                                                 end_color="000000", fill_type="solid")

                start_row = max_row + 1

            ajustar_colunas(ws_presenca)

            ws_alunos = wb.create_sheet(title='Alunos')
            ws_alunos.cell(row=1, column=1).value = 'ID'
            ws_alunos.cell(row=1, column=2).value = 'Nome'
            ws_alunos.cell(row=1, column=3).value = 'CPF'
            ws_alunos.cell(row=1, column=4).value = 'Celular'
            ws_alunos.cell(row=1, column=5).value = 'Rua'
            ws_alunos.cell(row=1, column=6).value = 'Número'
            ws_alunos.cell(row=1, column=7).value = 'Bairro'
            ws_alunos.cell(row=1, column=8).value = 'Cidade'
            ws_alunos.cell(row=1, column=9).value = 'UF'
            ws_alunos.cell(row=1, column=10).value = 'É PCD?'

            alunos = Aluno.objects.filter(id_turma__in=turmas_aux).annotate(
                nome_ordenacao=Coalesce('nome_social', 'nome')).order_by('nome_ordenacao')

            for row, aluno in enumerate(alunos, start=2):
                ws_alunos.cell(row=row, column=1).value = aluno.pk
                ws_alunos.cell(row=row, column=2).value = aluno.nome_social if aluno.nome_social else aluno.nome
                ws_alunos.cell(row=row, column=3).value = aluno.cpf
                ws_alunos.cell(row=row, column=4).value = aluno.celular
                ws_alunos.cell(row=row, column=5).value = aluno.rua
                ws_alunos.cell(row=row, column=6).value = aluno.numero
                ws_alunos.cell(row=row, column=7).value = aluno.bairro
                ws_alunos.cell(row=row, column=8).value = aluno.cidade
                ws_alunos.cell(row=row, column=9).value = aluno.uf
                ws_alunos.cell(row=row, column=10).value = 'PCD' if aluno.pcd else ''

            ajustar_colunas(ws_alunos)

            filename = f"media/planilhas/presenca_{professor}_{curso_arq[curso]}.xlsx"
            wb.save(filename)


# Configuração do log
logger = logging.getLogger(__name__)
handler = logging.FileHandler('media/sorteio/sorteio.log', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
turmas = Turma.objects.all()
inscritos = Inscrito.objects.all()


def sortear():
    """
    Realiza o sorteio de inscritos em turmas conforme as regras especificadas.

    Este código é público para fins de transparência e validação do sorteio.

    - Para cada turma, o sorteio é realizado separadamente para vagas de cotas e de ampla concorrência.
    - Os inscritos sorteados são marcados como 'ja_sorteado' para evitar múltiplas seleções.
    - As operações são registradas em 'sorteio.log' para auditoria e verificação posterior.
    """

    logger.info("Inicio do sorteio")  # Mostra o início do sorteio no log

    for turma in turmas:  # Itera sobre todas as turmas
        logger.info(f"Turma: {turma.curso} - {turma.dias} - {turma.horario()}")  # Mostra no log a turma atual

        """
        Sorteio para vagas de cotas
        """

        vagas_cotas = turma.cotas()  # Pega o número de vagas para cotas (30% do total das vagas)
        inscritos_cotas = list(inscritos.filter(Q(id_turma=turma) & Q(Q(pcd=True) | Q(
            ps=True))))  # Pega todos os inscritos para a turma atual que sejam PCD ou participem de Programa Social

        if len(inscritos_cotas) <= vagas_cotas:  # Caso o número de inscritos cotistas para a turma atual seja menor
            # que o número de vagas para cotas da turma...
            sorteados_cotas = inscritos_cotas  # ... define os sorteados cotistas para a turma atual como todos os
            # inscritos para a turma atual
        else:  # Se não...
            sorteados_cotas = random.sample(inscritos_cotas,
                                            vagas_cotas)  # ... sorteia os inscritos de acordo com o número de vagas

        for sorteado in sorteados_cotas:  # Itera sobre todos os sorteados cotistas da turma atual
            logger.info(
                f'{sorteado.nome_social if sorteado.nome_social else sorteado.nome} - Cota')  # Mostra o nome civil ou social do sorteado no log
            sorteado.ja_sorteado = True  # Define o atributo ja_sorteado como verdadeiro
            sorteado.save()  # Salva a alteração

        """
        Sorteio para vagas de ampla concorrência
        """

        vagas_gerais = turma.ampla_conc()  # Pega o número de vagas para ampla concorrência (70% do total das vagas)
        inscritos_gerais = list(inscritos.filter(Q(id_turma=turma) & Q(
            ja_sorteado=False)))  # Pega todos os inscritos para a turma atual que não tenham sido sorteados ainda

        if len(inscritos_gerais) <= vagas_gerais:  # Caso o número de inscritos para a turma atual seja menor que o
            # número de vagas da turma...
            sorteados_gerais = inscritos_gerais  # ... define os sorteados para a turma atual como todos os inscritos
            # para a turma atual
        else:  # Se não...
            sorteados_gerais = random.sample(inscritos_gerais,
                                             vagas_gerais)  # ... sorteia os inscritos de acordo com o número de vagas

        for sorteado in sorteados_gerais:  # Itera sobre todos os sorteados de ampla concorrência da turma atual
            logger.info(
                f'{sorteado.nome_social if sorteado.nome_social else sorteado.nome} - Ampla concorrência')  # Mostra o nome civil ou social do sorteado no log
            sorteado.ja_sorteado = True  # Define o atributo ja_sorteado como verdadeiro
            sorteado.save()  # Salva a alteração

        logger.info('Fim da turma.')  # Mostra o final do sorteio da turma atual no log

        for i in range(5):  # Pula 5 linhas no log para melhorar a legibilidade
            logger.info("")

        """
        Por ser um loop, o processo se repetirá para todas as turmas 
        """

    logger.info("Fim do sorteio")  # Mostra o fim do sorteio no log