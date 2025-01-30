from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('inscricao/', inscricao, name='inscricao'),
    path('editais/', editais, name='editais'),
    path('resultado/', resultado, name='resultado'),
    path('resultado/<int:turma_id>/', resultado, name='resultado_id'),
    path('info_melhor_idade/', info_melhor_idade, name='info_melhor_idade'),
    path('info_basica/', info_basica, name='info_basica'),
    path('excel/', excel, name='excel'),
    path('power_bi/', power_bi, name='power_bi'),
    path('montagem/', montagem, name='montagem'),
    path('man_cel/', man_cel, name='man_cel'),
    path('robotica/', robotica, name='robotica'),
    path('design/', design, name='design'),
    path('educacao/', educacao, name='educacao'),
    path('gestao/', gestao, name='gestao'),
    path('marketing/', marketing, name='marketing'),
    path('marketing_emp_dig/', marketing_emp_dig, name='marketing_emp_dig'),
    path('blockchain/', blockchain, name='blockchain'),
    path('download_validadores', download_validadores, name='download_validadores'),
    path('download_1/', download_1, name='download_1'),
    path('download_2/', download_2, name='download_2'),
]
