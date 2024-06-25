import os
import django
from cpf_generator import CPF

# Configuração do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'incubadora.settings')
django.setup()

from database.models import Inscrito

for inscrito in Inscrito.objects.all():
    cpf = inscrito.cpf
    inscrito.cpf = CPF.format(cpf)
    inscrito.save()