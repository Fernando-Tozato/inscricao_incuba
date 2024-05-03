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
from database.views import TurmaViewSet, InscritoViewSet, SorteadoViewSet, AlunoViewSet

router = DefaultRouter()

router.register(r'turma', TurmaViewSet, basename='turma')
router.register(r'inscrito', InscritoViewSet, basename='inscrito')
router.register(r'sorteado', SorteadoViewSet, basename='sorteado')
router.register(r'aluno', AlunoViewSet, basename='aluno')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('accounts/', include('allauth.urls')),
    path('externo/', include('externo.urls')),
    path('interno/', include('interno.urls')),
]
