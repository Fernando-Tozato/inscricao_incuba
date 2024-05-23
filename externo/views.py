from django.shortcuts import render
import json
from django.http import JsonResponse
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ValidationError
from django.db.models import Q
from database.models import Inscrito, Turma

def inscricao(request):
    return render(request, 'inscricao.html')

@csrf_protect
def validar_inscricao(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            nome = data['nome']
            nome_pesquisa = data['nome_pesquisa']
            nome_social = data['nome_social']
            nome_social_pesquisa = data['nome_social_pesquisa']
            nascimento = data['nascimento']
            cpf = data['cpf']
            rg = data['rg']
            data_emissao = data['data_emissao']
            orgao_emissor = data['orgao_emissor']
            uf_emissao = data['uf_emissao']
            filiacao = data['filiacao']
            escolaridade = data['escolaridade']
            email = data['email']
            telefone = data['telefone']
            celular = data['celular']
            cep = data['cep']
            rua = data['rua']
            numero = data['numero']
            complemento = data['complemento']
            bairro = data['bairro']
            cidade = data['cidade']
            uf = data['uf']
            id_turma = data['id_turma']
            
            inscrito = Inscrito(
                nome = nome,
                nome_pesquisa = nome_pesquisa,
                nome_social = nome_social,
                nome_social_pesquisa = nome_social_pesquisa,
                nascimento = nascimento,
                cpf = cpf,
                rg = rg,
                data_emissao = data_emissao,
                orgao_emissor = orgao_emissor,
                uf_emissao = uf_emissao,
                filiacao = filiacao,
                escolaridade = escolaridade,
                email = email,
                telefone = telefone,
                celular = celular,
                cep = cep,
                rua = rua,
                numero = numero,
                complemento = complemento,
                bairro = bairro,
                cidade = cidade,
                uf = uf,
                id_turma = id_turma
            )
            
            try:
                inscrito.full_clean()
                inscrito.save()
                return render(request, 'enviado.html')
            except ValidationError as e:
                return JsonResponse({'error': e.message_dict}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Dados JSON inválidos'}, status=400)
    else:
        return JsonResponse({'error': 'Método não permitido.'}, status=405)

@csrf_protect
def verificar_cpf(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cpf = data['cpf']
            inscrito = Inscrito.objects.filter(cpf=cpf)
            if inscrito:
                return JsonResponse({'response': False}, status=200)
            else:
                return JsonResponse({'response': True}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Dados JSON inválidos'}, status=400)
    else:
        return JsonResponse({'error': 'Método não permitido.'}, status=405)

@csrf_protect
def busca_cursos(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            escolaridade = data['escolaridade']
            idade = data['idade']
            
            turmas = Turma.objects.filter(Q(escolaridade__lte=escolaridade) & Q(idade__lte=idade))
            cursos = []
            for turma in turmas:
                if turma.curso not in cursos:
                    cursos.append(turma.curso)
            if len(turmas) != 0:
                return JsonResponse({'cursos': cursos}, status=200)
            else:
                return JsonResponse({'error': 'Nenhuma turma encontrada.'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Dados JSON inválidos'}, status=400)
    else:
        return JsonResponse({'error': 'Método não permitido.'}, status=405)

def busca_dias(request):
    pass

def busca_horarios(request):
    pass