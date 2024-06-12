from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login, name='login'),
    path('cadastro/', cadastro, name='cadastro'),
    path('pagina_inicial/', pagina_inicial, name='pagina_inicial'),
    path('matricula/novo/', matricula_novo, name='matricula_novo'),
    path('matricula/existente/<int:inscrito_id>/', matricula_existente, name='matricula_existente'),
    path('matricula/criar/', matricula_criar, name='matricula_criar'),
    path('verificar_cpf/', verificar_cpf, name='verificar_cpf'),
    path('enviado/', enviado, name='enviado'),
    path('turma/', turma, name='turma'),
    path('turma/novo/', turma_novo, name='turma_novo'),
    path('turma/editar/<int:turma_id>/', turma_editar, name='turma_editar'),
    path('turma/criar/', turma_criar, name='turma_criar'),
    path('turma/view_editar/', turma_view_editar, name='turma_view_editar'),
    path('sorteio/', sorteio, name='sorteio'),
    path('sorteio/sortear/', sortear, name='sortear'),
]