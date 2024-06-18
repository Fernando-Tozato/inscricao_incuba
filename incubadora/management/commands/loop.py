from django.core.management.base import BaseCommand
import logging
from database.models import Controle
from django.utils import timezone
from interno.tasks import sortear

class Command(BaseCommand):
    help = 'Run an infinite loop performing some operations'

    def handle(self, *args, **kwargs):
        logger = logging.getLogger(__name__)
        handler = logging.FileHandler('loop.log')
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        logger.info("Starting infinite loop")

        try:
            while True:
                controle = Controle.objects.first()
                agora = timezone.now()
                if agora >= controle.sorteio_data: # type: ignore
                    sortear()
        except KeyboardInterrupt:
            logger.info("Infinite loop interrupted and stopped")
