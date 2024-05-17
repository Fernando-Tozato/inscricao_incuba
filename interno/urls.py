from django.urls import path
from .views import login, cadastro, matricula_novo, matricula_existente, pagina_inicial, turma, turma_novo, turma_editar, pesquisa_cpf, pesquisa_nome

urlpatterns = [
    path('login/', login, name='login'),
    path('cadastro/', cadastro, name='cadastro'),
    path('matricula/novo/', matricula_novo, name='matricula_novo'),
    path('matricula/existente/', matricula_existente, name='matricula_existente'),
    path('pagina_inicial/', pagina_inicial, name='pagina_inicial'),
    path('turma', turma, name='turma'),
    path('turma/novo', turma_novo, name='turma_novo'),
    path('turma/editar', turma_editar, name='turma_editar'),
    path('pesquisa_cpf/', pesquisa_cpf, name='pesquisa_cpf'),
    path('pesquisa_nome/', pesquisa_nome, name='pesquisa_nome'),
]