from django.shortcuts import render
from rest_framework import viewsets
from .models import Turma, Inscrito
from .serializers import TurmaSerializer, InscritoSerializer

def inscricao(request):
    return render(request, 'inscricao.html')

def enviado(request):
    return render(request, 'enviado.html')

class TurmaViewSet(viewsets.ModelViewSet):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer

class InscritoViewSet(viewsets.ModelViewSet):
    queryset = Inscrito.objects.all()
    serializer_class = InscritoSerializer