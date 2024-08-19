from rest_framework import viewsets

from .serializers import *


class InscritoViewSet(viewsets.ModelViewSet):
    queryset = Inscrito.objects.all()
    serializer_class = InscritoSerializer


class TurmaViewSet(viewsets.ModelViewSet):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer


class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer


class ControleViewSet(viewsets.ModelViewSet):
    queryset = Controle.objects.all()
    serializer_class = ControleSerializer
