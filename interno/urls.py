from django.urls import path
from .views import *

urlpatterns = [
    path('', busca_de_inscrito, name='busca_de_inscrito'),
    path('matricula/', matricula, name='matricula'),
    path('matricula/<int:inscrito_id>/', matricula, name='matricula_inscrito'),
    path('enviado/', enviado, name='enviado_int'),
    path('busca_aluno/', busca_de_aluno, name='busca_de_aluno'),
    path('editar_aluno/<int:aluno_id>/', editar_aluno, name='editar_aluno'),
    path('turma/', turma, name='turma'),
    path('turma/novo/', turma_criar, name='turma_novo'),
    path('turma/criar/', turma_criar, name='turma_criar'),
    path('turma/editar/<int:turma_id>/', turma_editar, name='turma_editar'),
    path('turma/excluir/<int:turma_id>/', turma_excluir, name='turma_excluir'),
    path('controle/', controle, name='controle'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('reset_password/', reset_password_view, name='reset_password'),
    path('reset_password_sent/', reset_password_sent_view, name='reset_password_sent'),
    path('reset/<uidb64>/<token>/', reset_password_confirm_view, name='password_reset_confirm'),
    path('reset_password_complete/', reset_password_complete_view, name='reset_password_complete'),
    path('planilhas/', planilhas, name='planilhas'),
    path('planilha_coord/', planilha_coord, name='planilha_coord'),
    path('sorteio/', sorteio, name='sorteio'),
]
