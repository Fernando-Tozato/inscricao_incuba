from database.models import *
from django.db.models import Q
import random, logging
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, Alignment, PatternFill
from datetime import datetime, timedelta

def avisar_sorteados():
    pass

def gerar_planilhas():
    aulas_inicio = Controle.objects.first().aulas_inicio # type: ignore
    aulas_fim = Controle.objects.first().aulas_fim # type: ignore
    
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
        'Marketing Digital': 'mark_digital',
        'Marketing Empreendedor': 'mark_emp'
    }
    
    professores = Turma.objects.values('professor').distinct()
    print(professores)
    for professor in professores:
        professor = professor['professor']
        print(professor)
        cursos = Turma.objects.filter(professor=professor).values('curso').distinct()
        print(cursos)
        for curso in cursos:
            curso = curso['curso']
            print(curso)
            turmas = Turma.objects.filter(Q(professor=professor) & Q(curso=curso))
            
            wb = Workbook()
            sheet_name = 'Presença'
            ws = wb.create_sheet(title=sheet_name)
            
            print(turmas)
            start_row = 1
            for turma in turmas:
                header = f"{turma.dias} {turma.horario()}"
                ws.merge_cells(start_row=start_row, start_column=1, end_row=start_row, end_column=2)
                ws.cell(row=start_row, column=1).value = header
                ws.cell(row=start_row, column=1).font = Font(bold=True)
                ws.cell(row=start_row, column=1).alignment = Alignment(horizontal="center")

                ws.cell(row=start_row + 1, column=1).value = 'id'
                ws.cell(row=start_row + 1, column=2).value = 'Nome'
                
                for col in range(3, (aulas_fim - aulas_inicio).days + 3):
                    dia_aula = aulas_inicio + timedelta(days=col - 3)
                    coluna = get_column_letter(col)
                    ws.cell(row=start_row + 1, column=col).value = dia_aula.strftime('%d/%m')

                for col in range(1, ws.max_column + 1):
                    cell = ws.cell(row=start_row + 1, column=col)
                    cell.font = Font(bold=True)
                    cell.alignment = Alignment(horizontal="center")

                alunos = Aluno.objects.filter(id_turma=turma)

                idx=0
                
                for idx, aluno in enumerate(alunos, start=start_row + 2):
                    ws.cell(row=idx, column=1).value = aluno.pk
                    ws.cell(row=idx, column=2).value = aluno.nome

                max_row = idx + 1
                for col in range(1, ws.max_column + 1):
                    ws.cell(row=max_row, column=col).fill = PatternFill(start_color="000000", end_color="000000", fill_type="solid")

                start_row = max_row + 1
                    
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
    
    logger.info("Inicio do sorteio") # Mostra o início do sorteio no log
    
    for turma in turmas: # Itera sobre todas as turmas
        logger.info(f"Turma: {turma.curso} - {turma.dias} - {turma.horario()}") # Mostra no log a turma atual
        
        
        """
        Sorteio para vagas de cotas
        """
        
        vagas_cotas = turma.cotas() # Pega o número de vagas para cotas (30% do total das vagas)
        inscritos_cotas = list(inscritos.filter(Q(id_turma=turma) & Q(Q(pcd=True) | Q(ps=True)))) # Pega todos os inscritos para a turma atual que sejam PCD ou participem de Programa Social
        
        if len(inscritos_cotas) <= vagas_cotas: # Caso o número de inscritos cotistas para a turma atual seja menor que o número de vagas para cotas da turma...
            sorteados_cotas = inscritos_cotas # ... define os sorteados cotistas para a turma atual como todos os inscritos para a turma atual
        else: # Se não...
            sorteados_cotas = random.sample(inscritos_cotas, vagas_cotas) # ... sorteia os inscritos de acordo com o número de vagas
        
        for sorteado in sorteados_cotas: # Itera sobre todos os sorteados cotistas da turma atual
            logger.info(f'{sorteado.nome_social if sorteado.nome_social else sorteado.nome} - Cota') # Mostra o nome civil ou social do sorteado no log
            sorteado.ja_sorteado = True # Define o atributo ja_sorteado como verdadeiro
            sorteado.save() # Salva a alteração
        
        
        """
        Sorteio para vagas de ampla concorrência
        """
        
        vagas_gerais = turma.ampla_conc() # Pega o número de vagas para ampla concorrência (70% do total das vagas)
        inscritos_gerais = list(inscritos.filter(Q(id_turma=turma) & Q(ja_sorteado=False))) # Pega todos os inscritos para a turma atual que não tenham sido sorteados ainda
        
        if len(inscritos_gerais) <= vagas_gerais: # Caso o número de inscritos para a turma atual seja menor que o número de vagas da turma...
            sorteados_gerais = inscritos_gerais # ... define os sorteados para a turma atual como todos os inscritos para a turma atual
        else: # Se não...
            sorteados_gerais = random.sample(inscritos_gerais, vagas_gerais) # ... sorteia os inscritos de acordo com o número de vagas
        
        for sorteado in sorteados_gerais: # Itera sobre todos os sorteados de ampla concorrência da turma atual
            logger.info(f'{sorteado.nome_social if sorteado.nome_social else sorteado.nome} - Ampla concorrência') # Mostra o nome civil ou social do sorteado no log
            sorteado.ja_sorteado = True # Define o atributo ja_sorteado como verdadeiro
            sorteado.save() # Salva a alteração
        
        logger.info('Fim da turma.') # Mostra o final do sorteio da turma atual no log
        
        for i in range(5): # Pula 5 linhas no log para melhorar a legibilidade
            logger.info("")
        
        """
        Por ser um loop, o processo se repetirá para todas as turmas 
        """
        
    
    logger.info("Fim do sorteio") # Mostra o fim do sorteio no log
