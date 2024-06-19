from database.models import Inscrito, Turma
from django.db.models import Q
import random, logging


# Configuração do log
logger = logging.getLogger(__name__)
handler = logging.FileHandler('sorteio.log')
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
    
    logger.info("Inicio do sorteio")
    
    for turma in Turma.objects.all():
        logger.info(f"Turma: {turma.curso} - {turma.dias} - {turma.horario()}")
        
        # Sorteio para vagas de cotas
        vagas_cotas = turma.cotas()
        inscritos_cotas = list(Inscrito.objects.filter(Q(id_turma=turma) & Q(Q(pcd=True) | Q(ps=True))))
        sorteados_cotas = random.sample(inscritos_cotas, vagas_cotas)
        
        for sorteado in sorteados_cotas:
            logger.info(f'{sorteado.nome if sorteado.nome_social != '' else sorteado.nome_social}')
            sorteado.ja_sorteado = True
            sorteado.save()
        
        # Sorteio para vagas de ampla concorrência
        vagas_gerais = turma.ampla_conc()
        inscritos_gerais = list(Inscrito.objects.filter(Q(id_turma=turma) & Q(ja_sorteado=False)))
        sorteados_gerais = random.sample(inscritos_gerais, vagas_gerais)
        
        for sorteado in sorteados_gerais:
            logger.info(f'{sorteado.nome if sorteado.nome_social != '' else sorteado.nome_social}')
            sorteado.ja_sorteado = True
            sorteado.save()
    
    logger.info("Fim do sorteio")
