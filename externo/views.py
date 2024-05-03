from django.shortcuts import render

def inscricao(request):
    return render(request, 'inscricao.html')

def enviado(request):
    return render(request, 'enviado.html')