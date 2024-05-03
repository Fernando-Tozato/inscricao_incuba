from django.urls import path
from .views import inscricao, enviado

urlpatterns = [
    path('inscricao/', inscricao, name='inscricao'),
    path('enviado/', enviado, name='enviado'),
]