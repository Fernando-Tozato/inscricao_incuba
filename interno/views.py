import sqlite3
from django.shortcuts import render
from database.models import Inscrito

conn = sqlite3.Connection('db.sqlite3')
cursor = conn.cursor()

def matricula_novo(request):
    return render(request, 'matricula_novo.html')

def matricula_existente(request):
    return render(request, 'matricula_existente.html')

def login(request):
    return render(request, 'login.html')

def cadastro(request):
    return render(request, 'cadastro.html')

def pagina_inicial(request):
    if request.method == 'POST':
        parte_do_cpf = request.POST.get('cpf', '')
        resultados = Inscrito.objects.filter(cpf__contains=parte_do_cpf)

        return render(request, 'pagina_inicial.html', {'resultados': resultados})

    return render(request, 'pagina_inicial.html')
