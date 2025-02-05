"""
URL configuration for inscricao_incuba project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from database.views import *
from externo.views import aviso

router = DefaultRouter()

router.register(r'unidade', UnidadeViewSet, basename='unidade')
router.register(r'curso', CursoViewSet, basename='curso')
router.register(r'turma', TurmaViewSet, basename='turma')
router.register(r'inscrito', InscritoViewSet, basename='inscrito')
router.register(r'aluno', AlunoViewSet, basename='aluno')
router.register(r'controle', ControleViewSet, basename='controle')

urlpatterns = [
    path('admin/', aviso),
    path('', aviso, name='externo'),
    path('interno/', aviso, name='interno'),
]
