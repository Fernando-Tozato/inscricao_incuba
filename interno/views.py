from django.shortcuts import render

def matricula(request):
    return render(request, 'matricula.html')

def login(request):
    return render(request, 'login.html')

def cadastro(request):
    return render(request, 'cadastro.html')