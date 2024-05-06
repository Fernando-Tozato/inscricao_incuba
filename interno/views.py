from django.shortcuts import render
from forms import Busca_CPF

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
        form = Busca_CPF(request.POST)
        if 
    return render(request, 'pagina_inicial.html', {'form': form})