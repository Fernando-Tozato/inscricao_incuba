from django.urls import path
from .views import login, cadastro, matricula

urlpatterns = [
    path('login/', login, name='login'),
    path('cadastro/', cadastro, name='cadastro'),
    path('matricula/', matricula, name='matricula')
]