import os
import random
from datetime import timedelta
from logging import Logger

from celery import shared_task

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q, QuerySet
from django.db.models.functions import Coalesce
from django.template.loader import render_to_string
from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
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
    """
    Ajusta a largura das colunas com base no conteúdo.
    """
    for col in ws.columns:
        max_length = 0
        column = get_column_letter(col[0].column)  # Obtém a letra da coluna
        for cell in col:
            try:
                if cell.value:
                    cell_length = len(str(cell.value))
                    if cell_length > max_length:
                        max_length = cell_length
            except:
                pass
        adjusted_width = max_length + 2
        ws.column_dimensions[column].width = adjusted_width


def criar_folha_presenca(wb, turmas, aulas_inicio, aulas_fim):
    """
    Cria a folha de presença no workbook.
    """
    ws_presenca = wb.create_sheet(title='Presença')

    # Definir estilos para a linha escura
    dark_fill = PatternFill(start_color="4F4F4F", end_color="4F4F4F", fill_type="solid")

    start_row = 1
    sabados = []
    domingos = []

    # Cabeçalhos Gerais
    headers = [
        ('Presente', 'P', '6aa84f'),
        ('Faltoso', 'F', 'cc0000'),
        ('Faltas Justificadas', 'J', 'ff9900'),  # Nova legenda 'J'
        ('Fim de Semana', 'S/D', '3d85c6'),
        ('Feriado', 'H', '8e7cc3')
    ]

    current_column = 3  # Começando da coluna 3
    for header, short, color in headers:
        ws_presenca.merge_cells(start_row=start_row, start_column=current_column, end_row=start_row,
                                end_column=current_column + 1)
        ws_presenca.cell(row=start_row, column=current_column).value = header
        ws_presenca.cell(row=start_row, column=current_column).font = Font(bold=True)
        ws_presenca.cell(row=start_row, column=current_column).alignment = Alignment(horizontal="center")

        ws_presenca.cell(row=start_row, column=current_column + 2).value = short
        ws_presenca.cell(row=start_row, column=current_column + 2).font = Font(bold=True)
        ws_presenca.cell(row=start_row, column=current_column + 2).alignment = Alignment(horizontal="center")
        ws_presenca.cell(row=start_row, column=current_column + 2).fill = PatternFill(start_color=color,
                                                                                      end_color=color,
                                                                                      fill_type="solid")

        current_column += 4  # Avança para a próxima seção

    # Títulos de Coluna
    ws_presenca.cell(row=start_row + 1, column=1).value = 'ID'
    ws_presenca.cell(row=start_row + 1, column=2).value = 'Nome'

    total_aulas = (aulas_fim - aulas_inicio).days + 1  # Inclusivo
    data_aulas = [aulas_inicio + timedelta(days=i) for i in range(total_aulas)]

    dia_coluna_map = {}

    for i, dia_aula in enumerate(data_aulas, start=3):
        ws_presenca.cell(row=start_row + 1, column=i).value = dia_aula.strftime('%d/%m')
        ws_presenca.cell(row=start_row + 1, column=i).font = Font(bold=True)
        ws_presenca.cell(row=start_row + 1, column=i).alignment = Alignment(horizontal="center")

        if dia_aula.weekday() == 5:  # Sábado
            sabados.append(i)
        elif dia_aula.weekday() == 6:  # Domingo
            domingos.append(i)

    # Formatação de Cabeçalho
    for col in range(1, 3 + total_aulas):
        cell = ws_presenca.cell(row=start_row + 1, column=col)
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center")

    # Regras de Formatação Condicional
    range_str = f"C3:{get_column_letter(ws_presenca.max_column)}1000"  # Ajuste o número de linhas conforme necessário

    # Definir as cores para as legendas
    red_fill = PatternFill(start_color="cc0000", end_color="cc0000", fill_type="solid")
    green_fill = PatternFill(start_color="6aa84f", end_color="6aa84f", fill_type="solid")
    orange_fill = PatternFill(start_color="ff9900", end_color="ff9900", fill_type="solid")
    blue_fill = PatternFill(start_color="3d85c6", end_color="3d85c6", fill_type="solid")
    purple_fill = PatternFill(start_color="8e7cc3", end_color="8e7cc3", fill_type="solid")

    bold_font = Font(bold=True)

    # Regras para 'F', 'P', 'J'
    ws_presenca.conditional_formatting.add(range_str,
                                           CellIsRule(operator='equal', formula=['"F"'], fill=red_fill, font=bold_font))
    ws_presenca.conditional_formatting.add(range_str,
                                           CellIsRule(operator='equal', formula=['"P"'], fill=green_fill, font=bold_font))
    ws_presenca.conditional_formatting.add(range_str,
                                           CellIsRule(operator='equal', formula=['"J"'], fill=orange_fill, font=bold_font))
    ws_presenca.conditional_formatting.add(range_str,
                                           CellIsRule(operator='equal', formula=['"S"'], fill=blue_fill, font=bold_font))
    ws_presenca.conditional_formatting.add(range_str,
                                           CellIsRule(operator='equal', formula=['"D"'], fill=blue_fill, font=bold_font))
    ws_presenca.conditional_formatting.add(range_str,
                                           CellIsRule(operator='equal', formula=['"H"'], fill=purple_fill, font=bold_font))

    # Adicionar bordas grossas para a linha escura
    thin_border = Border(left=Side(style='thin'),
                         right=Side(style='thin'),
                         top=Side(style='thin'),
                         bottom=Side(style='thin'))

    # Preenchimento das Turmas
    current_row = start_row + 2
    for turma in turmas:
        # Título da Turma
        header = f'{turma.dias} {turma.horario()}'
        ws_presenca.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=2)
        ws_presenca.cell(row=current_row, column=1).value = header
        ws_presenca.cell(row=current_row, column=1).font = bold_font
        ws_presenca.cell(row=current_row, column=1).alignment = Alignment(horizontal="center")
        current_row += 1

        # Alunos da Turma
        alunos = Aluno.objects.filter(id_turma=turma).annotate(
            nome_ordenacao=Coalesce('nome_social', 'nome')).order_by('nome_ordenacao')

        for aluno in alunos:
            ws_presenca.cell(row=current_row, column=1).value = aluno.pk
            ws_presenca.cell(row=current_row, column=2).value = aluno.nome_social if aluno.nome_social else aluno.nome
            ws_presenca.cell(row=current_row, column=1).alignment = Alignment(horizontal="center")
            ws_presenca.cell(row=current_row, column=2).alignment = Alignment(horizontal="left")

            # Inicializa as células de presença
            for col in range(3, 3 + total_aulas):
                ws_presenca.cell(row=current_row, column=col).value = ""
                ws_presenca.cell(row=current_row, column=col).alignment = Alignment(horizontal="center")

            current_row += 1

        # Inserir uma linha escura após a turma
        ws_presenca.append([])  # Adiciona uma linha vazia
        for col in range(1, 3 + total_aulas):
            cell = ws_presenca.cell(row=current_row, column=col)
            cell.fill = dark_fill
            cell.border = thin_border
        current_row += 1

    ajustar_colunas(ws_presenca)
    return ws_presenca


def criar_folha_alunos(wb, turmas):
    """
    Cria a folha de alunos no workbook.
    """
    ws_alunos = wb.create_sheet(title='Alunos')
    headers = ['ID', 'Nome', 'CPF', 'Celular', 'Rua', 'Número', 'Bairro', 'Cidade', 'UF', 'É PCD?']
    for col_num, header in enumerate(headers, start=1):
        ws_alunos.cell(row=1, column=col_num).value = header
        ws_alunos.cell(row=1, column=col_num).font = Font(bold=True)
        ws_alunos.cell(row=1, column=col_num).alignment = Alignment(horizontal="center")

    alunos = Aluno.objects.filter(id_turma__in=turmas).annotate(
        nome_ordenacao=Coalesce('nome_social', 'nome')).order_by('nome_ordenacao')

    for row_num, aluno in enumerate(alunos, start=2):
        ws_alunos.cell(row=row_num, column=1).value = aluno.pk
        ws_alunos.cell(row=row_num, column=2).value = aluno.nome_social if aluno.nome_social else aluno.nome
        ws_alunos.cell(row=row_num, column=3).value = aluno.cpf_formatado()
        ws_alunos.cell(row=row_num, column=4).value = aluno.celular
        ws_alunos.cell(row=row_num, column=5).value = aluno.rua
        ws_alunos.cell(row=row_num, column=6).value = aluno.numero
        ws_alunos.cell(row=row_num, column=7).value = aluno.bairro
        ws_alunos.cell(row=row_num, column=8).value = aluno.cidade
        ws_alunos.cell(row=row_num, column=9).value = aluno.uf
        ws_alunos.cell(row=row_num, column=10).value = 'PCD' if aluno.pcd else ''

        # Alinhamento das células
        for col in range(1, 11):
            ws_alunos.cell(row=row_num, column=col).alignment = Alignment(horizontal="left")

    ajustar_colunas(ws_alunos)
    return ws_alunos


def gerar_planilhas():
    """
    Gera planilhas Excel para cada professor e curso ministrado.
    Cada planilha contém duas folhas: Presença e Alunos.
    """
    try:
        controle = Controle.objects.first()
        if not controle:
            print("Nenhum controle encontrado.")
            return

        aulas_inicio = controle.aulas_inicio
        aulas_fim = controle.aulas_fim

        curso_arq = {
            'Informática para Iniciantes e Melhor Idade': 'info_melhor_idade',
            'Informática Básica': 'info_basica',
            'Excel': 'excel',
            'Montagem e Manutenção de Computadores': 'montagem',
            'Robótica e Automação: Módulo 01': 'robotica_01',
            'Robótica e Automação: Módulo 02': 'robotica_02',
            'Robótica e Automação: Módulo 03': 'robotica_03',
            'Design e Modelagem 3D: Módulo 01': 'design_01',
            'Design e Modelagem 3D: Módulo 02': 'design_02',
            'Gestão de Pessoas': 'gestao_pessoas',
            'Educação Financeira': 'educ_finan',
            'Marketing Digital': 'mark_digital',
            'Marketing Empreendedor': 'mark_emp'
        }

        turmas = Turma.objects.all()
        professores = set(turma.professor for turma in turmas)  # Elimina duplicatas

        for professor in professores:
            # Filtra turmas do professor
            turmas_professor = turmas.filter(professor=professor)
            cursos = set(turma.curso for turma in turmas_professor)  # Elimina duplicatas

            for curso in cursos:
                if curso not in curso_arq:
                    print(f"Curso '{curso}' não mapeado em curso_arq. Pulando...")
                    continue  # Pula cursos que não estão mapeados

                # Filtra turmas específicas do curso e professor
                turmas_aux = turmas_professor.filter(curso=curso)

                if not turmas_aux.exists():
                    continue  # Pula se não houver turmas

                wb = Workbook()
                # Remove a folha padrão criada pelo Workbook
                default_sheet = wb.active
                wb.remove(default_sheet)

                # Cria as folhas necessárias
                criar_folha_presenca(wb, turmas_aux, aulas_inicio, aulas_fim)
                criar_folha_alunos(wb, turmas_aux)

                # Definir caminho e nome do arquivo
                nome_arquivo = f"presenca_{professor}_{curso_arq[curso]}.xlsx"
                caminho_arquivo = os.path.join('media', 'planilhas', nome_arquivo)

                # Garantir que o diretório exista
                os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)

                # Salvar o workbook
                wb.save(caminho_arquivo)
                print(f"Planilha salva: {caminho_arquivo}")

    except Exception as e:
        print(f"Ocorreu um erro durante a geração das planilhas: {e}")


def sortear(logger: Logger, turmas: QuerySet[Turma], inscritos: QuerySet[Inscrito]):
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


@shared_task(bind=True)
def test_func(self):
    for i in range(10):
        print(i)
    return 'Done'