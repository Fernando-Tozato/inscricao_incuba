from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login, name='login'),
    path('cadastro/', cadastro, name='cadastro'),
    path('matricula/novo/', matricula_novo, name='matricula_novo'),
    path('matricula/existente/', matricula_existente, name='matricula_existente'),
    path('pagina_inicial/', pagina_inicial, name='pagina_inicial'),
    path('pagina_inicial/pesquisa_cpf/', pesquisa_cpf, name='pesquisa_cpf'),
    path('pagina_inicial/pesquisa_nome/', pesquisa_nome, name='pesquisa_nome'),
    path('turma/', turma, name='turma'),
    path('turma/novo/', turma_novo, name='turma_novo'),
    path('turma/editar/<int:turma_id>/', turma_editar, name='turma_editar'),
    path('turma/criar/', turma_criar, name='turma_criar'),
    path('turma/view_editar/', turma_view_editar, name='turma_view_editar'),
]