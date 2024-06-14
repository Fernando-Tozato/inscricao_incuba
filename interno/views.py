from django.shortcuts import render, get_object_or_404
import json, random, pandas
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ValidationError
from django.db.models import Q
from database.models import Inscrito, Turma, Aluno


def login(request):
    return render(request, 'interno/login.html')

def cadastro(request):
    return render(request, 'interno/cadastro.html')

def pagina_inicial(request):
    parametro = request.GET.get('parametro', '')
    valor = request.GET.get('valor', '')
        
    if parametro and valor:
        if parametro == 'nome':
            resultados_nome_social = Inscrito.objects.filter(nome_social_pesquisa__contains=valor)
            resultados_nome = Inscrito.objects.filter(nome_pesquisa__contains=valor).filter(Q(nome_social='') | Q(nome_social__isnull=True))
            inscritos = resultados_nome_social | resultados_nome
        else:
            inscritos = Inscrito.objects.filter(cpf__contains=valor)
            if len(valor) in [3, 7]: valor += '.'
            elif len(valor) == 11: valor += '-'
        return render(request, 'interno/pagina_inicial.html', {'inscritos': inscritos, 'busca': valor})
    else:
        return render(request, 'interno/pagina_inicial.html')

def matricula_novo(request):
    return render(request, 'interno/matricula_novo.html')

def matricula_existente(request, inscrito_id):
    inscrito = get_object_or_404(Inscrito, id=inscrito_id)
    turma = inscrito.id_turma
    return render(request, 'interno/matricula_existente.html', {'inscrito': inscrito, 'turma': turma})

def matricula_criar(request):
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
            
            aluno = Aluno(
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
                aluno.save()
                return JsonResponse({'success': 'Sucesso no envio'}, status=200)
            except ValidationError as e:
                return JsonResponse({'error': e.message_dict}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Dados JSON inválidos'}, status=400)
    else:
        return JsonResponse({'error': 'Método não permitido.'}, status=405)

@csrf_protect
def matricula_sorteados(request):
    pass

@csrf_protect
def matricula_geral(request):
    pass

@csrf_protect
def verificar_cpf(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cpf = data['cpf']
            aluno = Aluno.objects.filter(cpf=cpf)
            
            if len(aluno) == 0:
                return JsonResponse({'response': False}, status=200)
            else:
                return JsonResponse({'response': True}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Dados JSON inválidos'}, status=400)
    else:
        return JsonResponse({'error': 'Método não permitido.'}, status=405)

def enviado(request):
    return render(request, 'interno/enviado_int.html')

def turma(request):
    return render(request, 'interno/turma.html', {'turmas': Turma.objects.all()})

def turma_novo(request):
    return render(request, 'interno/turma_novo.html')

def turma_editar(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    return render(request, 'interno/turma_editar.html', {'turma': turma})

@csrf_protect
def turma_criar(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            curso = data['curso']
            dias = data['dias']
            entrada = datetime.strptime(data['entrada'], '%H:%M')
            saida = datetime.strptime(data['saida'], '%H:%M')
            vagas = data['vagas']
            escolaridade = data['escolaridade']
            idade = data['idade']
            professor = data['professor']
            
            turma = Turma(
                curso = curso,
                dias = dias,
                horario_entrada = entrada,
                horario_saida = saida,
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
        return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_protect
def turma_view_editar(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Dados JSON inválidos'}, status=400)

        turma_id = data.get('id')
        if not turma_id:
            return JsonResponse({'error': 'ID inválido'}, status=400)

        try:
            turma = Turma.objects.get(id=turma_id)
        except Turma.DoesNotExist:
            return JsonResponse({'error': 'Turma não encontrada'}, status=404)

        updated_fields = []
        for field, value in data.items():
            if field == 'id':
                continue
            if hasattr(turma, field) and getattr(turma, field) != value:
                setattr(turma, field, value)
                updated_fields.append(field)

        if not updated_fields:
            return JsonResponse({'Sucesso': 'Sem mudanças detectadas'}, status=200)

        turma.save(update_fields=updated_fields)

        return JsonResponse({'Sucesso': 'Sucesso na atualização'}, status=200)
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=400)

def controle(request):
    return render(request, 'interno/controle.html')

@csrf_protect
def sortear(request):
    for turma in Turma.objects.all():
        vagas_cotas = turma.cotas()
        inscritos_pcd = list(Inscrito.objects.filter(Q(id_turma = turma) & Q(Q(pcd=True) | Q(ps=True))))
        sorteados_pcd = random.sample(inscritos_pcd, vagas_cotas)
        
        for sorteado in sorteados_pcd:
            sorteado.ja_sorteado = True
        
        vagas_gerais = turma.ampla_conc()
        inscritos_gerais = list(Inscrito.objects.filter(Q(id_turma = turma) & Q(ja_sorteado=False)))
        sorteados_gerais = random.sample(inscritos_gerais, vagas_gerais)
        
        for sorteado in sorteados_gerais:
            sorteado.ja_sorteado = True
        
        sorteados = sorteados_pcd + sorteados_gerais
        
        
