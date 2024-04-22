from urllib import request
from django.shortcuts import render
from rest_framework import viewsets
from .models import Turma, Contato, Endereco, Aluno
from .serializers import TurmaSerializer, ContatoSerializer, EnderecoSerializer, AlunoSerializer

def index(request):
    turmas = Turma.objects.all()
    return render(request, 'index.html', {'turmas': turmas})

class TurmaViewSet(viewsets.ModelViewSet):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer

class ContatoViewSet(viewsets.ModelViewSet):
    queryset = Contato.objects.all()
    serializer_class = ContatoSerializer

class EnderecoViewSet(viewsets.ModelViewSet):
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer