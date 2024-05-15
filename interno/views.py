from django.shortcuts import render
from database.models import Inscrito
from django.http import JsonResponse

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
