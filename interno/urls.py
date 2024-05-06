from django.urls import path
from .views import login, cadastro, matricula_novo, matricula_existente, pagina_inicial

urlpatterns = [
    path('login/', login, name='login'),
    path('cadastro/', cadastro, name='cadastro'),
    path('matricula/novo/', matricula_novo, name='matricula_novo'),
    path('matricula/existente/', matricula_existente, name='matricula_existente'),
    path('pagina_inicial/', pagina_inicial, name='pagina_inicial'),
]