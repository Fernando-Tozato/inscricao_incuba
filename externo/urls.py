from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('inscricao/', inscricao, name='inscricao'),
    path('editais/', editais, name='editais'),
    path('resultado/', resultado, name='resultado'),
    path('resultado/<int:turma_id>/', resultado, name='resultado_id'),
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
    path('download_2/', download_2, name='download_2'),
]
