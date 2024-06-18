from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site

from .forms import *
from database.models import Inscrito, Turma, Aluno

import json, random
from datetime import datetime

def grupo_necessario(user):
    return user.groups.filter(Q(name='Coord_Ped') | Q(name='Admin')).exists()

@login_required
def busca_de_inscrito(request):
    parametro = request.GET.get('parametro', '')
    valor = request.GET.get('valor', '')
        
    if parametro and valor:
        if parametro == 'nome':
            resultados_nome_social = Inscrito.objects.filter(nome_social_pesquisa__contains=valor)
            resultados_nome = Inscrito.objects.filter(nome_pesquisa__contains=valor).filter(Q(nome_social='') | Q(nome_social__isnull=True))
            inscritos = resultados_nome_social | resultados_nome
            valor = valor.capitalize()
        elif parametro == 'cpf':
            inscritos = Inscrito.objects.filter(cpf__contains=valor)
            if len(valor) in [3, 7]: valor += '.'
            elif len(valor) == 11: valor += '-'
        else:
            return JsonResponse({'error': 'Parâmetro não suportado.'}, status=405)
        return render(request, 'interno/busca_de_inscrito.html', {'inscritos': inscritos, 'busca': valor})
    else:
        return render(request, 'interno/busca_de_inscrito.html')

def matricula_novo(request):
    return render(request, 'interno/matricula_novo.html')

def matricula_existente(request, inscrito_id):
    inscrito = get_object_or_404(Inscrito, id=inscrito_id)
    turma = inscrito.id_turma
    return render(request, 'interno/matricula_existente.html', {'inscrito': inscrito, 'turma': turma})

@csrf_protect
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

@login_required
def enviado(request):
    return render(request, 'interno/enviado_int.html')

@user_passes_test(grupo_necessario)
@login_required
def turma(request):
    return render(request, 'interno/turma.html', {'turmas': Turma.objects.all()})

@user_passes_test(grupo_necessario)
@login_required
def turma_novo(request):
    return render(request, 'interno/turma_novo.html')

@user_passes_test(grupo_necessario)
@login_required
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

@user_passes_test(grupo_necessario)
@login_required
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
        
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('busca_de_inscrito')
    else:
        form = LoginForm()
    return render(request, 'interno/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('busca_de_inscrito')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'interno/register.html', {'form': form})

def reset_password_view(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            users = User.objects.filter(email=email)
            if users.exists():
                for user in users:
                    subject = "Alteração de Senha"
                    email_template_name = "interno/password_reset_email.html"
                    c = {
                        "email": user.email,
                        'domain': get_current_site(request).domain,
                        'site_name': 'Incubadora de Robótica',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email_content = render_to_string(email_template_name, c)
                    email_message = EmailMultiAlternatives(subject, '', 'incuba.robotica.auto@gmail.com', [user.email])
                    email_message.attach_alternative(email_content, "text/html")
                    email_message.send()
                return redirect('reset_password_sent')
    else:
        form = CustomPasswordResetForm()
    return render(request, 'interno/password_reset.html', {'form': form})

def reset_password_sent_view(request):
    return render(request, 'interno/password_reset_sent.html')

def reset_password_confirm_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        print('ok')
        if request.method == 'POST':
            print('ok')
            form = CustomSetPasswordForm(user, request.POST)
            print('ok')
            if form.is_valid():
                form.save()
                print('ok')
                return redirect('reset_password_complete')
        else:
            form = CustomSetPasswordForm(user)
        return render(request, 'interno/password_reset_confirm.html', {'form': form})
    else:
        return render(request, 'interno/password_reset_invalid.html')

def reset_password_complete_view(request):
    return render(request, 'interno/password_reset_complete.html')
