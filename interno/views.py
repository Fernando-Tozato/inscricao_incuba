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
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Sum
from django.db.utils import IntegrityError
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlsafe_base64_decode
from django.db.models.functions import TruncDate
from django.db.models import Count

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
            #
            # for i in range(num_threads): thread = threading.Thread(target=avisar_sorteados, args=[request,
            # inscritos[num_inscritos_por_thread * i: num_inscritos_por_thread * (i + 1)]]) threads.append(thread)
            #
            # if i + 1 == num_threads: thread = threading.Thread(target=avisar_sorteados, args=[request, inscritos[
            # num_inscritos_por_thread * (i + 1):]]) threads.append(thread)
            #
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
def estatisticas(request):
    return render(request, 'interno/estatisticas.html')


def get_estatisticas(request):
    inscritos = Inscrito.objects.all() \
        .annotate(date=TruncDate('data_inscricao')) \
        .values('date') \
        .annotate(count=Count('id')) \
        .order_by('date')

    alunos = Aluno.objects.all() \
        .annotate(date=TruncDate('data_matricula')) \
        .values('date') \
        .annotate(count=Count('id')) \
        .order_by('date')

    data = {
        'inscritos': list(inscritos),
        'alunos': list(alunos)
    }

    return JsonResponse(data)


@login_required
def busca_de_inscrito(request):
    vagas = Turma.objects.values('curso__nome').annotate(vagas=(Sum('vagas') - Sum('num_alunos')))

    context = {'vagas': vagas}

    if request.method == 'POST':
        form = BuscaForm(request.POST)
        if form.is_valid():
            busca = form.cleaned_data['busca']

            if any(char.isdigit() for char in busca):
                busca = re.sub(r'\D', '', busca)
                resultado_cpf = Inscrito.objects.filter(cpf__contains=busca)
                resultado_inscricao = Inscrito.objects.filter(numero_inscricao__contains=busca)
                inscritos = resultado_cpf | resultado_inscricao
            else:
                busca = unidecode(busca.upper())
                resultados_nome_social = Inscrito.objects.filter(nome_social_pesquisa__contains=busca)
                resultados_nome = (Inscrito.objects.filter(nome_pesquisa__contains=busca)
                                   .filter(Q(nome_social='') | Q(nome_social__isnull=True)))
                inscritos = resultados_nome_social | resultados_nome

            inscritos = verificar_inscritos(request, inscritos)

            context.update({'inscritos': inscritos})
        context.update({'form': form})
    else:
        context.update({'form': BuscaForm})
    return render(request, 'interno/busca_de_inscrito.html', context)


@login_required
def matricula(request, inscrito_id=None):
    print('matricula', inscrito_id)

    turmas = Turma.objects.select_related('unidade', 'curso').all()

    dados = []
    for turma in turmas:
        dados.append({
            'unidade_id': turma.unidade.id,
            'unidade_nome': turma.unidade.nome,
            'curso_id': turma.curso.id,
            'curso_nome': turma.curso.nome,
            'curso_idade': turma.curso.idade,
            'curso_escolaridade': turma.curso.escolaridade,
            'turma_id': turma.id,
            'turma_dias': turma.dias,
            'turma_horario': turma.horario()
        })

    context = {'dados': dados}

    inscrito = get_object_or_404(Inscrito, id=inscrito_id) if inscrito_id else None

    if request.method == 'POST':
        form = MatriculaForm(request.POST, inscrito=inscrito.dict_for_matricula() if inscrito_id else None)
        context.update({'form': form})

        if form.is_valid():
            try:
                aluno = form.save()
            except ValidationError as e:
                messages.error(request, f'Aluno já matriculado.\n{e}')
            except IntegrityError as e:
                messages.error(request, f'Aluno já matriculado.\n{e}')
            except Exception as e:
                messages.error(request, f'Erro:\n{e}')
            else:
                aluno.id_turma.num_alunos += 1
                aluno.id_turma.save()
                return render(request, 'interno/enviado_int.html')

        else:
            print('invalid')
            print(form.errors)
    else:
        context.update({'form': MatriculaForm(inscrito=inscrito.dict_for_matricula() if inscrito_id else None)})
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
    turmas = Turma.objects.select_related('unidade', 'curso').all()

    dados = []
    for turma in turmas:
        dados.append({
            'unidade_id': turma.unidade.id,
            'unidade_nome': turma.unidade.nome,
            'curso_id': turma.curso.id,
            'curso_nome': turma.curso.nome,
            'curso_idade': turma.curso.idade,
            'curso_escolaridade': turma.curso.escolaridade,
            'turma_id': turma.id,
            'turma_dias': turma.dias,
            'turma_horario': turma.horario()
        })

    context = {'dados': dados}

    aluno = get_object_or_404(Aluno, id=aluno_id) if aluno_id else None

    if aluno:
        aluno.id_turma.num_alunos -= 1
        aluno.id_turma.save()

    if request.method == 'POST':
        form = MatriculaForm(request.POST, instance=aluno)
        context.update({'form': form})

        if form.is_valid():
            try:
                if is_allowed(request.user):
                    aluno = form.save()
                else:
                    messages.error(request, 'Você não tem permissão para executar essa ação.')
            except ValidationError as e:
                messages.error(request, f'Erro de validação: {e}')
            except IntegrityError as e:
                messages.error(request, f'Erro de integridade: {e}')
            except Exception as e:
                messages.error(request, f'Erro ao salvar dados: {e}')
            else:
                aluno.id_turma.num_alunos += 1
                aluno.id_turma.save()
                return redirect('busca_de_aluno')
        else:
            messages.error(request, 'Formulário inválido. Verifique os erros abaixo.')
    else:
        form = MatriculaForm(instance=aluno)
        context.update({'form': form})

    return render(request, 'interno/editar_aluno.html', context)


@login_required
def unidade(request):
    return render(request, 'interno/ver_unidades.html', {'unidades': Unidade.objects.all()})


@user_passes_test(is_allowed)
@login_required
def unidade_criar(request):
    context = {}

    if request.method == 'POST':
        form = UnidadeForm(request.POST)
        context.update({'form': form})
        if form.is_valid():
            try:
                form.save()
            except IntegrityError as e:
                messages.error(request,
                               f'Houve um problema com os dados inseridos. Contate a equipe de suporte.\n\nErro: {e}')
            except Exception as e:
                messages.error(request, f'Erro: {e}')
            else:
                return redirect('unidade')

    else:
        context.update({'form': UnidadeForm})

    return render(request, 'interno/unidade.html', context)


@user_passes_test(is_allowed)
@login_required
def unidade_editar(request, unidade_id=None):
    context = {}

    unidade = get_object_or_404(Unidade, id=unidade_id) if unidade_id else None
    context.update({'id_unidade': unidade.id})

    if request.method == 'POST':
        form = UnidadeForm(request.POST, instance=unidade)
        context.update({'form': form})

        if form.is_valid():
            try:
                if is_allowed(request.user):
                    form.save()

                    return redirect('unidade')
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
        form = UnidadeForm(instance=unidade)
        context.update({'form': form})

    return render(request, 'interno/unidade.html', context)


@user_passes_test(is_allowed)
@login_required
def unidade_excluir(request, unidade_id=None):
    unidade = get_object_or_404(Unidade, id=unidade_id) if unidade_id else None

    if request.method == 'POST':
        unidade.delete()
        return redirect('unidade')
    return redirect('unidade_editar', unidade_id=unidade.id)


@login_required
def curso(request):
    return render(request, 'interno/ver_cursos.html', {'cursos': Curso.objects.all()})


@user_passes_test(is_allowed)
@login_required
def curso_criar(request):
    context = {}

    if request.method == 'POST':
        form = CursoForm(request.POST)
        context.update({'form': form})
        if form.is_valid():

            try:
                form.save()
            except IntegrityError as e:
                messages.error(request,
                               f'Houve um problema com os dados inseridos. Contate a equipe de suporte.\n\nErro: {e}')
            except Exception as e:
                messages.error(request, f'Erro: {e}')
            else:
                return redirect('curso')

    else:
        context.update({'form': CursoForm})

    return render(request, 'interno/curso.html', context)


@user_passes_test(is_allowed)
@login_required
def curso_editar(request, curso_id=None):
    context = {}

    curso = get_object_or_404(Curso, id=curso_id) if curso_id else None
    context.update({'id_curso': curso.id})

    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        context.update({'form': form})

        if form.is_valid():
            try:
                if is_allowed(request.user):
                    form.save()
                    form.save_m2m()

                    messages.success(request, 'Dados da curso atualizados com sucesso!')
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
        form = CursoForm(instance=curso)
        context.update({'form': form})

    return render(request, 'interno/curso.html', context)


@user_passes_test(is_allowed)
@login_required
def curso_excluir(request, curso_id=None):
    curso = get_object_or_404(Curso, id=curso_id) if curso_id else None

    if request.method == 'POST':
        curso.delete()
        return redirect('curso')
    return redirect('curso_editar', curso_id=curso.id)


@login_required
def turma(request):
    return render(request, 'interno/ver_turmas.html', {'turmas': Turma.objects.all()})


@user_passes_test(is_allowed)
@login_required
def turma_criar(request):
    context = {"cursos": list(Curso.objects.all().values('id', 'unidades__id')),
               'unidades': list(Unidade.objects.all().values('id', 'nome'))}

    if request.method == 'POST':
        form = TurmaForm(request.POST)
        context.update({'form': form})
        if form.is_valid():
            try:
                form.save()
            except IntegrityError as e:
                messages.error(request,
                               f'Houve um problema com os dados inseridos. Contate a equipe de suporte.\n\nErro: {e}')
            except Exception as e:
                messages.error(request, f'Erro: {e}')
            else:
                return redirect('turma')

    else:
        context.update({'form': TurmaForm})

    return render(request, 'interno/turma.html', context)


@user_passes_test(is_allowed)
@login_required
def turma_editar(request, turma_id=None):
    cursos = list(Curso.objects.all().values('id', 'unidades__id'))
    unidades = list(Unidade.objects.all().values('id', 'nome'))
    context = {"cursos": json.dumps(cursos, cls=DjangoJSONEncoder),
               "unidades": json.dumps(unidades, cls=DjangoJSONEncoder)}

    turma = get_object_or_404(Turma, id=turma_id) if turma_id else None
    context.update({'id_turma': turma.id})

    if request.method == 'POST':
        form = TurmaForm(request.POST, instance=turma)
        context.update({'form': form})

        if form.is_valid():
            try:
                if is_allowed(request.user):
                    form.save()

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
        form = TurmaForm(instance=turma)
        context.update({'form': form})

    return render(request, 'interno/turma.html', context)


@user_passes_test(is_allowed)
@login_required
def turma_excluir(request, turma_id=None):
    turma = get_object_or_404(Turma, id=turma_id) if turma_id else None

    if request.method == 'POST':
        turma.delete()
        return redirect('turma')
    return redirect('turma_editar', turma_id=turma.id)


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
