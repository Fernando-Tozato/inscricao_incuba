from urllib import request
from django.shortcuts import render
from django.http import HttpResponseRedirect
from rest_framework import viewsets
from .models import Turma, Aluno
from .serializers import TurmaSerializer, AlunoSerializer

def index(request):
    return render(request, 'index.html')

def enviado(request):
    return render(request, 'enviado.html')

class TurmaViewSet(viewsets.ModelViewSet):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer