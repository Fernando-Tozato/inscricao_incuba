from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('inscricao/', inscricao, name='inscricao'),
    path('inscricao/enviado/', enviado, name='enviado_ext'),
    path('inscricao/validar/', validar_inscricao, name='validar_inscricao'),
    path('inscricao/verificar_cpf/', verificar_cpf, name='verificar_cpf'),
    path('inscricao/busca_cursos/', busca_cursos, name='busca_cursos'),
    path('inscricao/busca_dias/', busca_dias, name='busca_dias'),
    path('inscricao/busca_horarios/', busca_horarios, name='busca_horarios'),
    path('editais/', editais, name='editais'),
    path('resultado/', resultado, name='resultado'),
    path('resultado/<int:id_turma>/', resultado_id, name='resultado_id'),
    path('design/', design, name='design'),
    path('educacao/', educacao, name='educacao'),
    path('excel/', excel, name='excel'),
    path('gestao/', gestao, name='gestao'),
    path('info_basica/', info_basica, name='info_basica'),
    path('info_melhor_idade/', info_melhor_idade, name='info_melhor_idade'),
    path('marketing_digital/', marketing_digital, name='marketing_digital'),
    path('marketing_emp/', marketing_emp, name='marketing_emp'),
    path('montagem/', montagem, name='montagem'),
    path('robotica/', robotica, name='robotica'),
    path('download_validadores', download_validadores, name='download_validadores'),
    path('download_1/', download_1, name='download_1'),
]
