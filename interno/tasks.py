import logging
import random

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from openpyxl import Workbook

from interno.functions import *


def avisar_sorteados(request, emails, sorteado=False):
    controle = Controle.objects.first()

    if sorteado:
        email_template_name = "aviso_sorteado.html"
        c = {
            'domain': get_current_site(request).domain,
            'protocol': 'http',
            'data_matricula_inicio': controle.matricula_sorteados,  # type: ignore
            'data_matricula_fim': controle.matricula_fim,  # type: ignore
            'data_aulas_inicio': controle.aulas_inicio,  # type: ignore
        }
        email_content = render_to_string(email_template_name, c)

    else:
        email_template_name = 'aviso_nao_sorteado.html'
        c = {
            'domain': get_current_site(request).domain,
            'protocol': 'http',
            'data_matricula_inicio': controle.matricula_geral,  # type: ignore
            'data_matricula_fim': controle.matricula_fim,  # type: ignore
            'data_aulas_inicio': controle.aulas_inicio,  # type: ignore
        }
        email_content = render_to_string(email_template_name, c)

    email = EmailMessage(
        'Incubadora de Robótica',
        email_content,
        'nao-responda@incubarobotica.com.br',
        emails,
    )
    email.content_subtype = 'html'
    email.send()

    try:
        email.send()
        print('enviado')
    except Exception as e:
        print(e)

    print('Fim')
