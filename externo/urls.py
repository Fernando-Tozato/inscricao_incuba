from django.urls import path
from .views import inscricao, validar_inscricao, verificar_cpf, busca_cursos, busca_dias, busca_horarios

urlpatterns = [
    path('inscricao/', inscricao, name='inscricao'),
    path('validar/', validar_inscricao, name='validar_inscricao'),
    path('verificar_cpf/', verificar_cpf, name='verificar_cpf'),
    path('busca_cursos/', busca_cursos, name='busca_cursos'),
    path('busca_dias/', busca_dias, name='busca_dias'),
    path('busca_horarios/', busca_horarios, name='busca_horarios'),
]