from django.shortcuts import render
from rest_framework import viewsets
from .models import Turmas, Contatos, Enderecos, Alunos
from .serializers import TurmasSerializer, ContatosSerializer, EnderecosSerializer, AlunosSerializer

class TurmasViewSet(viewsets.ModelViewSet):
    queryset = Turmas.objects.all()
    serializer_class = TurmasSerializer

class ContatosViewSet(viewsets.ModelViewSet):
    queryset = Contatos.objects.all()
    serializer_class = ContatosSerializer

class EnderecosViewSet(viewsets.ModelViewSet):
    queryset = Enderecos.objects.all()
    serializer_class = EnderecosSerializer

class AlunosViewSet(viewsets.ModelViewSet):
    queryset = Alunos.objects.all()
    serializer_class = AlunosSerializer