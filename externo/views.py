from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ValidationError
from django.db.models import Q
from database.models import *
from django.utils import timezone

def home(request):
    return render(request, 'home.html')

def inscricao(request):
    agora = timezone.now()
    controle = Controle.objects.first()
    inicio = timezone.localtime(controle.inscricao_inicio) # type: ignore
    fim = timezone.localtime(controle.inscricao_fim) # type: ignore
    remanescente = timezone.localtime(controle.matricula_geral) # type: ignore
    
    if agora < inicio:
        return render(request, 'antes_inscricao.html', {'data': inicio})
    elif agora > fim:
        return render(request, 'depois_inscricao.html', {'data_inscricao': fim, 'data_remanescente': remanescente})
    return render(request, 'inscricao.html')

def enviado(request):
    return render(request, 'enviado_ext.html')

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
            data_emissao = data['data_emissao'] if data['data_emissao'] != '' else None
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
            id_turma = Turma.objects.filter(pk=data['id_turma'])[0]
            
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
                return JsonResponse({'success': 'Sucesso no envio'}, status=200)
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
            
            if len(inscrito) == 0:
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

@csrf_protect
def busca_dias(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            curso = data['curso']
            
            turmas = Turma.objects.filter(curso=curso)
            
            dias = []
            for turma in turmas:
                if turma.dias not in dias:
                    dias.append(turma.dias)
                    
            if len(turmas) != 0:
                return JsonResponse({'dias': dias}, status=200)
            else:
                return JsonResponse({'error': 'Nenhuma turma encontrada.'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Dados JSON inválidos'}, status=400)
    else:
        return JsonResponse({'error': 'Método não permitido.'}, status=405)

@csrf_protect
def busca_horarios(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            curso = data['curso']
            dias = data['dias']
            
            turmas = Turma.objects.filter(Q(curso=curso) & Q(dias=dias))
            
            horarios = []
            ids = []
            for turma in turmas:
                entrada = turma.horario_entrada.strftime('%H:%M')
                saida = turma.horario_saida.strftime('%H:%M')
                final = f'{entrada} - {saida}'
                if final not in horarios:
                    horarios.append(final)
                    ids.append(turma.pk)
                    
            if len(turmas) != 0:
                return JsonResponse({'horarios': horarios, 'ids': ids}, status=200)
            else:
                return JsonResponse({'error': 'Nenhuma turma encontrada.'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Dados JSON inválidos'}, status=400)
    else:
        return JsonResponse({'error': 'Método não permitido.'}, status=405)

def editais(request):
    return render(request, 'editais.html')

def resultado(request):
    return render(request, 'resultado.html')

def design(request):
    return render(request, 'cursos/design.html')

def educacao(request):
    return render(request, 'cursos/educacao.html')

def excel(request):
    return render(request, 'cursos/excel.html')

def gestao(request):
    return render(request, 'cursos/gestao.html')

def info_basica(request):
    return render(request, 'cursos/info_basica.html')

def info_melhor_idade(request):
    return render(request, 'cursos/info_melhor_idade.html')

def marketing_digital(request):
    return render(request, 'cursos/marketing_digital.html')

def marketing_emp(request):
    return render(request, 'cursos/marketing_emp.html')

def montagem(request):
    return render(request, 'cursos/montagem.html')

def robotica(request):
    return render(request, 'cursos/robotica.html')