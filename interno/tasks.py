from database.models import Inscrito, Turma
from django.db.models import Q
import random, logging


# Configuração do log
logger = logging.getLogger(__name__)
handler = logging.FileHandler('sorteio.log', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def sortear():
    """
    Realiza o sorteio de inscritos em turmas conforme as regras especificadas.
    
    Este código é público para fins de transparência e validação do sorteio.
    
    - Para cada turma, o sorteio é realizado separadamente para vagas de cotas e de ampla concorrência.
    - Os inscritos sorteados são marcados como 'ja_sorteado' para evitar múltiplas seleções.
    - As operações são registradas em 'sorteio.log' para auditoria e verificação posterior.
    """
    
    logger.info("Inicio do sorteio") # Mostra o início do sorteio no log
    
    for turma in Turma.objects.all(): # Itera sobre todas as turmas
        logger.info(f"Turma: {turma.curso} - {turma.dias} - {turma.horario()}") # Mostra no log a turma atual
        
        
        """
        Sorteio para vagas de cotas
        """
        
        vagas_cotas = turma.cotas() # Pega o número de vagas para cotas (30% do total das vagas)
        inscritos_cotas = list(Inscrito.objects.filter(Q(id_turma=turma) & Q(Q(pcd=True) | Q(ps=True)))) # Pega todos os inscritos para a turma atual que sejam PCD ou participem de Programa Social
        
        if len(inscritos_cotas) <= vagas_cotas: # Caso o número de inscritos cotistas para a turma atual seja menor que o número de vagas para cotas da turma...
            sorteados_cotas = inscritos_cotas # ... define os sorteados cotistas para a turma atual como todos os inscritos para a turma atual
        else: # Se não...
            sorteados_cotas = random.sample(inscritos_cotas, vagas_cotas) # ... sorteia os inscritos de acordo com o número de vagas
        
        for sorteado in sorteados_cotas: # Itera sobre todos os sorteados cotistas da turma atual
            logger.info(f'{sorteado.nome if sorteado.nome_social == '' else sorteado.nome_social} - Cota') # Mostra o nome civil ou social do sorteado no log
            sorteado.ja_sorteado = True # Define o atributo ja_sorteado como verdadeiro
            sorteado.save() # Salva a alteração
        
        
        """
        Sorteio para vagas de ampla concorrência
        """
        
        vagas_gerais = turma.ampla_conc() # Pega o número de vagas para ampla concorrência (70% do total das vagas)
        inscritos_gerais = list(Inscrito.objects.filter(Q(id_turma=turma) & Q(ja_sorteado=False))) # Pega todos os inscritos para a turma atual que não tenham sido sorteados ainda
        
        if len(inscritos_gerais) <= vagas_gerais: # Caso o número de inscritos para a turma atual seja menor que o número de vagas da turma...
            sorteados_gerais = inscritos_gerais # ... define os sorteados para a turma atual como todos os inscritos para a turma atual
        else: # Se não...
            sorteados_gerais = random.sample(inscritos_gerais, vagas_gerais) # ... sorteia os inscritos de acordo com o número de vagas
        
        for sorteado in sorteados_gerais: # Itera sobre todos os sorteados de ampla concorrência da turma atual
            logger.info(f'{sorteado.nome if sorteado.nome_social == '' else sorteado.nome_social} - Ampla concorrência') # Mostra o nome civil ou social do sorteado no log
            sorteado.ja_sorteado = True # Define o atributo ja_sorteado como verdadeiro
            sorteado.save() # Salva a alteração
        
        logger.info('Fim da turma.') # Mostra o final do sorteio da turma atual no log
        
        for i in range(5): # Pula 5 linhas no log para melhorar a legibilidade
            logger.info("")
        
        """
        Por ser um loop, o processo se repetirá para todas as turmas 
        """
        
    
    logger.info("Fim do sorteio") # Mostra o fim do sorteio no log
