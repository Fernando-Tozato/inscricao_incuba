import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'incubadora.settings')

app = Celery('incubadora')

# Configure o Celery diretamente com o broker URL do Redis
app.conf.update(
    broker_url='redis://127.0.0.1:6379',
    accept_content=['json'],
    result_serializer='json',
    task_serializer='json',
    timezone='America/Sao_Paulo',
    task_track_started=True,
    task_time_limit=30 * 60,
    broker_connection_retry_on_startup = True
)

# Carregue tarefas de todos os aplicativos Django registrados.
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
