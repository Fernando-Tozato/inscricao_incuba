from django.shortcuts import render, get_object_or_404
import json
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ValidationError
from django.db.models import Q
from database.models import Inscrito, Turma

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

def turma(request):
    return render(request, 'turma.html', {'turmas': Turma.objects.all()})

def turma_novo(request):
    return render(request, 'turma_novo.html')

def turma_editar(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    return render(request, 'turma_editar.html', {'turma':turma})

@csrf_protect
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

@csrf_protect
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

@csrf_protect
def turma_criar(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            curso = data['curso']
            dias = data['dias']
            entrada = datetime.strptime(data['entrada'], '%H:%M')
            saida = datetime.strptime(data['saida'], '%H:%M')
            horario = data['horario']
            vagas = data['vagas']
            escolaridade = data['escolaridade']
            idade = data['idade']
            professor = data['professor']
            
            turma = Turma(
                curso = curso,
                dias = dias,
                horario_entrada = entrada,
                horario_saida = saida,
                horario = horario,
                vagas = vagas,
                escolaridade = escolaridade,
                idade = idade,
                professor = professor
            )
            
            try:
                turma.full_clean()
                turma.save()
                return JsonResponse({'success': 'Sucesso no envio'}, status=200)
            except ValidationError as e:
                return JsonResponse({'error': e.message_dict}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Dados JSON inválidos'}, status=400)
    else:
        return JsonResponse({'error': 'Método não permitido.'}, status=405)

@csrf_protect
def turma_view_editar(request):
    pass