from django.shortcuts import render
from database.models import Inscrito
from django.http import JsonResponse
from django.db.models import Q

def matricula_novo(request):
    return render(request, 'matricula_novo.html')

def matricula_existente(request):
    return render(request, 'matricula_existente.html')

def login(request):
    return render(request, 'login.html')

def cadastro(request):
    return render(request, 'cadastro.html')

def pagina_inicial(request):
    return render(request, 'pagina_inicial.html')

def pesquisa_cpf(request):
    data = {}
    trecho_cpf = request.GET.get('cpf', '')
    resultados = Inscrito.objects.filter(cpf__contains=trecho_cpf)
    
    if len(resultados) == 0:
        return JsonResponse({'error': 'CPF não encontrado'})
    
    for i, resultado in enumerate(resultados):
        d = {
            'nome': resultado.nome,
            'nascimento': resultado.nascimento,
            'cpf': resultado.cpf,
            'filiacao': resultado.filiacao,
            'nome_social': resultado.nome_social,
        }
        data.update({str(i): d})
    return JsonResponse(data)

def pesquisa_nome(request):
    data = {}
    trecho_nome = request.GET.get('nome', '')
    
    resultados_nome_social = Inscrito.objects.filter(nome_social_pesquisa__contains=trecho_nome)
    resultados_nome = Inscrito.objects.filter(nome_pesquisa__contains=trecho_nome).filter(Q(nome_social='') | Q(nome_social__isnull=True))
    resultados = resultados_nome_social | resultados_nome
    
    if len(resultados) == 0:
        return JsonResponse({'error': 'Nome não encontrado'})
    
    for i, resultado in enumerate(resultados):
        d = {
            'nome': resultado.nome,
            'nascimento': resultado.nascimento,
            'cpf': resultado.cpf,
            'filiacao': resultado.filiacao,
            'nome_social': resultado.nome_social,
        }
        data.update({str(i): d})
    return JsonResponse(data)
