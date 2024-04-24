from urllib import request
from django.shortcuts import render
from django.http import HttpResponseRedirect
from rest_framework import viewsets
from .models import Turma, Aluno
from .serializers import TurmaSerializer, AlunoSerializer
from .forms import Form

def index(request):
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            return render(request, 'enviado.html')
    
    return render(request, 'index.html')

class TurmaViewSet(viewsets.ModelViewSet):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer