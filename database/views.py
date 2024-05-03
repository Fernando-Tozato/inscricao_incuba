from django.shortcuts import render
from rest_framework import viewsets
from .models import Inscrito, Turma, Sorteado, Aluno
from .serializers import InscritoSerializer, TurmaSerializer, SorteadoSerializer, AlunoSerializer

class InscritoViewSet(viewsets.ModelViewSet):
    queryset = Inscrito.objects.all()
    serializer_class = InscritoSerializer

class TurmaViewSet(viewsets.ModelViewSet):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer

class SorteadoViewSet(viewsets.ModelViewSet):
    queryset = Sorteado.objects.all()
    serializer_class = SorteadoSerializer

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer