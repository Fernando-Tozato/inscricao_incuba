import json
import logging
import threading
import time
import zipfile
from io import BytesIO

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.db.utils import IntegrityError
from django.http import HttpResponse, Http404
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.csrf import csrf_protect

from externo.functions import get_turmas_as_json
from incubadora.functions import load_form_to_object
from .criar_planilhas_coord import *
from .forms import *
from .functions import *
from .tasks import *


def loop(request):
    while True:
        time.sleep(1)
        data_sorteio = Controle.objects.first().sorteio_data  # type: ignore
        matricula_sorteados = Controle.objects.first().matricula_sorteados  # type: ignore
        agora = timezone.now()
        if agora >= data_sorteio:  # type: ignore
            if matricula_sorteados <= agora:
                print('tarde')
                break
            print('na hora')
            # sortear()

            # inscritos = Inscrito.objects.exclude(email__isnull=True)
            # num_threads = 10
            # num_inscritos_por_thread = len(inscritos) // num_threads
            # threads = []

            # for i in range(num_threads): thread = threading.Thread(target=avisar_sorteados, args=[request,
            # inscritos[num_inscritos_por_thread * i: num_inscritos_por_thread * (i + 1)]]) threads.append(thread)

            # if i + 1 == num_threads: thread = threading.Thread(target=avisar_sorteados, args=[request, inscritos[
            # num_inscritos_por_thread * (i + 1):]]) threads.append(thread)

            # for thread in threads:
            #     thread.daemon = True
            #     thread.start()

            inscritos = Inscrito.objects.exclude(email__isnull=True)

            sorteados = inscritos.filter(ja_sorteado=True)
            nao_sorteados = inscritos.filter(ja_sorteado=False)

            emails_sorteados = [sorteado.email for sorteado in sorteados]
            emails_nao_sorteados = [nao_sorteado.email for nao_sorteado in nao_sorteados]

            avisar_sorteados(request, ['tozato.fernando2004@gmail.com'], True)
            # avisar_sorteados(request, emails_nao_sorteados, False)

            break
        print('cedo')


@login_required
def busca_de_inscrito(request):
    vagas = Turma.objects.values('curso').annotate(vagas=(Sum('vagas') - Sum('num_alunos')))

    context = {'vagas': vagas}

    if request.method == 'POST':
        form = BuscaForm(request.POST)
        if form.is_valid():
            busca = form.cleaned_data['busca']

            if any(char.isalpha() for char in busca):
                busca = unidecode(busca.upper())
                resultados_nome_social = Inscrito.objects.filter(nome_social_pesquisa__contains=busca)
                resultados_nome = (Inscrito.objects.filter(nome_pesquisa__contains=busca)
                                   .filter(Q(nome_social='') | Q(nome_social__isnull=True)))
                inscritos = resultados_nome_social | resultados_nome
            else:
                busca = re.sub(r'\D', '', busca)

                inscritos = Inscrito.objects.filter(cpf__contains=busca)

            inscritos = verificar_inscritos(request, inscritos)

            context.update({'inscritos': inscritos})
        context.update({'form': form})
    else:
        context.update({'form': BuscaForm})
    return render(request, 'interno/busca_de_inscrito.html', context)


@login_required
def matricula(request, inscrito_id=None):
    turmas: str = get_turmas_as_json(['curso', 'dias', 'horario', 'idade', 'escolaridade'])
    context: dict[str: str | MatriculaForm] = {'turmas': turmas}

    if request.method == 'POST':
        form = MatriculaForm(request.POST, inscrito=get_object_or_404(Inscrito, id=inscrito_id) if inscrito_id else None)
        context.update({'form': form})

        print(request.POST)

        if form.is_valid():
            aluno = load_form_to_object(form, Aluno)

            try:
                if matricula_valida(request):
                    aluno.id_turma.num_alunos += 1

                    aluno.full_clean()
                    aluno.save()

                    aluno.id_turma.full_clean()
                    aluno.id_turma.save()
                else:
                    messages.error(request, 'Turma cheia.')
                    return render(request, 'interno/matricula.html', context)
            except ValidationError as e:
                messages.error(request, f'Aluno já matriculado.')
            except IntegrityError as e:
                messages.error(request, f'Erro de integridade: {e}')
            except Exception as e:
                messages.error(request, f'Erro: {e}')
            else:
                return render(request, 'interno/enviado_int.html')

        else:
            print('invalid')
            print(form.errors)
    else:
        context.update({'form': MatriculaForm(inscrito=get_object_or_404(Inscrito, id=inscrito_id) if inscrito_id else None)})
    return render(request, 'interno/matricula.html', context)


@login_required
def enviado(request):
    return render(request, 'interno/enviado_int.html')


@login_required
def busca_de_aluno(request):
    context = {}

    if request.method == 'POST':
        form = BuscaForm(request.POST)
        if form.is_valid():
            busca = form.cleaned_data['busca']

            if any(char.isalpha() for char in busca):
                busca = unidecode(busca.upper())
                resultados_nome_social = Aluno.objects.filter(nome_social_pesquisa__contains=busca)
                resultados_nome = (Aluno.objects.filter(nome_pesquisa__contains=busca)
                                   .filter(Q(nome_social='') | Q(nome_social__isnull=True)))
                alunos = resultados_nome_social | resultados_nome
            else:
                busca = re.sub(r'\D', '', busca)

                alunos = Aluno.objects.filter(cpf__contains=busca)

            context.update({'alunos': alunos})
        context.update({'form': form})
    else:
        context.update({'form': BuscaForm})
    return render(request, 'interno/busca_de_aluno.html', context)


@login_required
def editar_aluno(request, aluno_id=None):
    turmas: str = get_turmas_as_json(['curso', 'dias', 'horario', 'idade', 'escolaridade'])
    context: dict[str: str | MatriculaForm] = {'turmas': turmas}

    aluno = get_object_or_404(Aluno, id=aluno_id) if aluno_id else None

    turma_old = aluno.id_turma

    if request.method == 'POST':
        form = MatriculaForm(request.POST, inscrito=aluno)
        context.update({'form': form})

        if form.is_valid():
            try:
                # Atualizar manualmente os campos do objeto Aluno
                aluno.nome = form.cleaned_data['nome']
                aluno.nome_social = form.cleaned_data['nome_social']
                aluno.nascimento = datetime.datetime.strptime(form.cleaned_data['nascimento'], '%d/%m/%Y')
                aluno.cpf = re.sub(r'\D', '', form.cleaned_data['cpf'])
                aluno.rg = form.cleaned_data['rg']
                aluno.data_emissao = datetime.datetime.strptime(form.cleaned_data['data_emissao'], '%d/%m/%Y') if \
                form.cleaned_data['data_emissao'] else None
                aluno.orgao_emissor = form.cleaned_data['orgao_emissor']
                aluno.uf_emissao = form.cleaned_data['uf_emissao']
                aluno.filiacao = form.cleaned_data['filiacao']
                aluno.escolaridade = form.cleaned_data['escolaridade']
                aluno.observacoes = form.cleaned_data['observacoes']
                aluno.email = form.cleaned_data['email']
                aluno.telefone = form.cleaned_data['telefone']
                aluno.celular = form.cleaned_data['celular']
                aluno.cep = form.cleaned_data['cep']
                aluno.rua = form.cleaned_data['rua']
                aluno.numero = form.cleaned_data['numero']
                aluno.complemento = form.cleaned_data['complemento']
                aluno.bairro = form.cleaned_data['bairro']
                aluno.cidade = form.cleaned_data['cidade']
                aluno.uf = form.cleaned_data['uf']
                aluno.pcd = form.cleaned_data['pcd']
                aluno.ps = form.cleaned_data['ps']

                # Verificando os dados da turma
                curso = form.cleaned_data['curso']
                dias = form.cleaned_data['dias']
                horario = form.cleaned_data['horario']
                horario_entrada = horario[:5]
                horario_saida = horario[8:]

                # Buscar a turma com base nos critérios
                id_turma = Turma.objects.filter(
                    Q(curso=curso) &
                    Q(dias=dias) &
                    Q(horario_entrada=horario_entrada) &
                    Q(horario_saida=horario_saida)
                ).first()

                if id_turma and matricula_valida(request):
                    aluno.id_turma = id_turma

                    aluno.full_clean()
                    aluno.save()

                    print(f'\n\n\n\nold: {turma_old.pk}\nnew: {id_turma.pk}')
                    if turma_old != id_turma:
                        print("diferente")
                        turma_old.num_alunos -= 1
                        print(f'old: {turma_old.num_alunos}')
                        turma_old.full_clean()
                        turma_old.save()

                    # Atualizar a turma
                    id_turma.num_alunos += 1
                    print(f'new: {id_turma.num_alunos}')
                    id_turma.full_clean()
                    id_turma.save()

                    messages.success(request, 'Dados do aluno atualizados com sucesso!')
                    return render(request, 'interno/enviado_int.html')
                else:
                    messages.error(request, 'Você não tem permissão para executar essa ação.')
            except ValidationError as e:
                messages.error(request, f'Erro de validação: {e}')
            except IntegrityError as e:
                messages.error(request, f'Erro de integridade: {e}')
            except Exception as e:
                messages.error(request, f'Erro ao salvar dados: {e}')
        else:
            messages.error(request, 'Formulário inválido. Verifique os erros abaixo.')
    else:
        # Preencher o formulário com os dados do aluno existente
        form = MatriculaForm(inscrito=aluno)
        context.update({'form': form})

    return render(request, 'interno/editar_aluno.html', context)


@login_required
def turma(request):
    return render(request, 'interno/turma.html', {'turmas': Turma.objects.all()})


@user_passes_test(is_allowed)
@login_required
def turma_novo(request):
    context = {}

    if request.method == 'POST':
        form = TurmaForm(request.POST)
        context.update({'form': form})
        if form.is_valid():
            turma = load_form_to_object(form, Turma)

            try:
                turma.full_clean()
                turma.save()
            except IntegrityError as e:
                messages.error(request,
                               f'Houve um problema com os dados inseridos. Contate a equipe de desenvolvimento.')
            except Exception as e:
                messages.error(request, f'Erro: {e}')
            else:
                return redirect('turma')

    else:
        context.update({'form': TurmaForm})

    return render(request, 'interno/turma_form.html', context)


@user_passes_test(is_allowed)
@login_required
def turma_editar(request, turma_id=None):
    context = {}

    turma = get_object_or_404(Turma, id=turma_id) if turma_id else None

    if request.method == 'POST':
        form = TurmaForm(request.POST, turma=turma)
        context.update({'form': form})

        if form.is_valid():
            try:
                turma.curso = form.cleaned_data['curso']
                turma.professor = form.cleaned_data['professor']
                turma.dias = form.cleaned_data['dias']
                turma.horario_entrada = form.cleaned_data['horario_entrada']
                turma.horario_saida = form.cleaned_data['horario_saida']
                turma.vagas = form.cleaned_data['vagas']
                turma.idade = form.cleaned_data['idade']
                turma.escolaridade = form.cleaned_data['escolaridade']

                if is_allowed(request):
                    turma.full_clean()
                    turma.save()

                    messages.success(request, 'Dados da turma atualizados com sucesso!')
                    return render(request, 'interno/enviado_int.html')
                else:
                    messages.error(request, 'Você não tem permissão para executar essa ação.')
            except ValidationError as e:
                messages.error(request, f'Erro de validação: {e}')
            except IntegrityError as e:
                messages.error(request, f'Erro de integridade: {e}')
            except Exception as e:
                messages.error(request, f'Erro ao salvar dados: {e}')
        else:
            messages.error(request, 'Formulário inválido. Verifique os erros abaixo.')
    else:
        # Preencher o formulário com os dados do aluno existente
        form = TurmaForm(turma=turma)
        context.update({'form': form})

    return render(request, 'interno/turma_form.html', context)


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
                curso=curso,
                dias=dias,
                horario_entrada=entrada,
                horario_saida=saida,
                vagas=vagas,
                escolaridade=escolaridade,
                idade=idade,
                professor=professor
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


@user_passes_test(is_allowed)
@login_required
def controle(request):
    controle = Controle.objects.first()

    if request.method == 'POST':
        inscricao_inicio = request.POST.get('inscricao_inicio')
        inscricao_fim = request.POST.get('inscricao_fim')
        sorteio_data = request.POST.get('sorteio_data')
        matricula_sorteados = request.POST.get('matricula_sorteados')
        matricula_geral = request.POST.get('matricula_geral')
        matricula_fim = request.POST.get('matricula_fim')
        aulas_inicio = request.POST.get('aulas_inicio')
        aulas_fim = request.POST.get('aulas_fim')

        if controle:
            controle.inscricao_inicio = inscricao_inicio
            controle.inscricao_fim = inscricao_fim
            controle.sorteio_data = sorteio_data
            controle.matricula_sorteados = matricula_sorteados
            controle.matricula_geral = matricula_geral
            controle.matricula_fim = matricula_fim
            controle.aulas_inicio = aulas_inicio
            controle.aulas_fim = aulas_fim
            controle.save()
        else:
            Controle.objects.create(
                inscricao_inicio=inscricao_inicio,
                inscricao_fim=inscricao_fim,
                sorteio_data=sorteio_data,
                matricula_sorteados=matricula_sorteados,
                matricula_geral=matricula_geral,
                matricula_fim=matricula_fim,
                aulas_inicio=aulas_inicio,
                aulas_fim=aulas_fim
            )

        thread = threading.Thread(target=loop, args=[request])
        thread.daemon = True
        thread.start()

        return redirect('busca_de_inscrito')

    return render(request, 'interno/controle.html', {'controle': controle})


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
    return render(request, 'interno/accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'interno/accounts/register.html', {'form': form})


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
                    email_message = EmailMultiAlternatives(subject, '', 'nao_responda@incubarobotica.com.br', [user.email])
                    email_message.attach_alternative(email_content, "text/html")
                    email_message.send()
                return redirect('reset_password_sent')
    else:
        form = CustomPasswordResetForm()
    return render(request, 'interno/accounts/password_reset.html', {'form': form})


def reset_password_sent_view(request):
    return render(request, 'interno/accounts/password_reset_sent.html')


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
        return render(request, 'interno/accounts/password_reset_confirm.html', {'form': form})
    else:
        return render(request, 'interno/accounts/password_reset_invalid.html')


def reset_password_complete_view(request):
    return render(request, 'interno/accounts/password_reset_complete.html')


def planilhas(request):
    planilhas_dir = os.path.join(settings.MEDIA_ROOT, 'planilhas')

    if not os.path.exists(planilhas_dir):
        print('planilhas não existe')
        raise Http404("A pasta 'planilhas' não foi encontrada")
    print('planilhas existe')

    filenames = os.listdir(planilhas_dir)

    if not filenames:
        print('planilhas vazio')
        gerar_planilhas()
        filenames = os.listdir(planilhas_dir)
        if not filenames:
            print('planilhas não geradas')
            raise Http404("Não foi possível gerar as planilhas")
        print('planilhas criadas')
    print('planilhas não vazio')

    zip_subdir = "planilhas"
    zip_filename = f"{zip_subdir}.zip"

    buffer = BytesIO()

    with zipfile.ZipFile(buffer, "w") as zf:
        for filename in filenames:
            file_path = os.path.join(planilhas_dir, filename)
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    zip_path = os.path.join(zip_subdir, filename)
                    zf.writestr(zip_path, f.read())
            else:
                raise Http404(f"{filename} não encontrado")

    buffer.seek(0)

    response = HttpResponse(buffer, content_type="application/zip")
    response['Content-Disposition'] = f'attachment; filename={zip_filename}'

    return response


def sorteio(request):
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler('media/sorteio/sorteio.log', encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    turmas = Turma.objects.all()
    inscritos = Inscrito.objects.all()

    print('inicio sorteio')
    sortear(logger, turmas, inscritos)
    print('fim sorteio')

    # inscritos = Inscrito.objects.exclude(email__isnull=True)
    #
    # sorteados = inscritos.filter(ja_sorteado=True)
    # nao_sorteados = inscritos.filter(ja_sorteado=False)
    #
    # emails_sorteados = [sorteado.email for sorteado in sorteados]
    # emails_nao_sorteados = [nao_sorteado.email for nao_sorteado in nao_sorteados]
    #
    # print(emails_sorteados)
    # print(emails_nao_sorteados)
    #
    # avisar_sorteados(request, emails_sorteados, True)
    # avisar_sorteados(request, emails_nao_sorteados, False)

    return redirect('resultado')


def planilha_coord(request):
    planilhas_dir = os.path.join(settings.MEDIA_ROOT, 'planilha_coord')

    if not os.path.exists(planilhas_dir):
        print('planilha_coord não existe')
        raise Http404("A pasta 'planilha_coord' não foi encontrada")
    print('planilha_coord existe')

    filenames = os.listdir(planilhas_dir)

    if not filenames:
        print('planilha_coord vazio')
        gerar_planilha_coord()
        filenames = os.listdir(planilhas_dir)
        if not filenames:
            print('planilha_coord não gerada')
            raise Http404("Não foi possível gerar a planilha")
        print('planilha_coord criadas')
    print('planilha_coord não vazio')

    zip_subdir = "planilha_coord"
    zip_filename = f"{zip_subdir}.zip"

    buffer = BytesIO()

    with zipfile.ZipFile(buffer, "w") as zf:
        for filename in filenames:
            file_path = os.path.join(planilhas_dir, filename)
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    zip_path = os.path.join(zip_subdir, filename)
                    zf.writestr(zip_path, f.read())
            else:
                raise Http404(f"{filename} não encontrado")

    buffer.seek(0)

    response = HttpResponse(buffer, content_type="application/zip")
    response['Content-Disposition'] = f'attachment; filename={zip_filename}'

    return response
