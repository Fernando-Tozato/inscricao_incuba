from django.urls import path
from .views import *

urlpatterns = [
    path('busca_de_inscrito/', busca_de_inscrito, name='busca_de_inscrito'),
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
    path('controle/', controle, name='controle'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('reset_password/', reset_password_view, name='reset_password'),
    path('reset_password_sent/', reset_password_sent_view, name='reset_password_sent'),
    path('reset/<uidb64>/<token>/', reset_password_confirm_view, name='password_reset_confirm'),
    path('reset_password_complete/', reset_password_complete_view, name='reset_password_complete'),
]
