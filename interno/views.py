from django.shortcuts import render
from rest_framework import viewsets
from .models import Sorteado, Aluno
from .serializers import SorteadoSerializer, AlunoSerializer

def inscricao(request):
    return render(request, 'inscricao.html')

def enviado(request):
    return render(request, 'enviado.html')

class SorteadoViewSet(viewsets.ModelViewSet):
    queryset = Sorteado.objects.all()
    serializer_class = SorteadoSerializer

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer