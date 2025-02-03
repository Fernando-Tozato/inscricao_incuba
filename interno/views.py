from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.db.utils import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import ensure_csrf_cookie

from .forms import *
from .functions import *
from .tasks import *


def test(request):
    agora = timezone.now()

    sortear.apply_async(eta=agora + timedelta(seconds=10))

    return HttpResponse("test")


@login_required
def estatisticas(request):
    controle = Controle.objects.first()
    if not controle:
        return redirect('controle_datetimes')
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

@never_cache
@ensure_csrf_cookie
# noinspection PyTypeChecker
@login_required
def inscrito(request):
    cursos = Curso.objects.values('id', 'nome')

    vagas = []

    for curso in cursos:
        turmas_centro = Turma.objects.filter(curso_id=curso['id'], unidade_id=1)
        turmas_inoa = Turma.objects.filter(curso_id=curso['id'], unidade_id=2)

        vagas_centro = 0
        vagas_inoa = 0
        for turma in turmas_centro:
            vagas_centro += turma.vagas_restantes()

        for turma in turmas_inoa:
            vagas_inoa += turma.vagas_restantes()

        vagas.append({
            'curso': curso['nome'],
            'vagas_centro': vagas_centro,
            'vagas_inoa': vagas_inoa
        })

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
    return render(request, 'interno/inscrito.html', context)

@never_cache
@ensure_csrf_cookie
@login_required
def matricula(request, inscrito_id=None):
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
def enviado_int(request):
    return render(request, 'interno/enviado_int.html')

@never_cache
@ensure_csrf_cookie
@user_passes_test(is_allowed)
@login_required
def aluno(request):
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
    return render(request, 'interno/aluno.html', context)

@never_cache
@ensure_csrf_cookie
@user_passes_test(is_allowed)
@login_required
def aluno_editar(request, aluno_id=None):
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

    aluno = None
    if aluno_id:
        aluno = get_object_or_404(Aluno, id=aluno_id)
        context.update({'id_aluno': aluno.id})

    if request.method == 'POST':
        form = MatriculaForm(request.POST, instance=aluno)
        context.update({'form': form})

        aluno.id_turma.num_alunos -= 1
        aluno.id_turma.save()

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
                return redirect('aluno')
        else:
            messages.error(request, 'Formulário inválido. Verifique os erros abaixo.')
    else:
        form = MatriculaForm(instance=aluno)
        context.update({'form': form})

    return render(request, 'interno/editar_aluno.html', context)

@never_cache
@ensure_csrf_cookie
@user_passes_test(is_allowed)
@login_required
def aluno_excluir(request, aluno_id=None):
    aluno = get_object_or_404(Aluno, id=aluno_id) if aluno_id else None

    if request.method == 'POST':
        aluno.delete()
        return redirect('aluno')
    return redirect('aluno_editar', aluno_id=aluno.id)


@user_passes_test(is_allowed)
@login_required
def unidade(request):
    return render(request, 'interno/ver_unidades.html', {'unidades': Unidade.objects.all()})

@never_cache
@ensure_csrf_cookie
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

@never_cache
@ensure_csrf_cookie
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

@never_cache
@ensure_csrf_cookie
@user_passes_test(is_allowed)
@login_required
def unidade_excluir(request, unidade_id=None):
    unidade = get_object_or_404(Unidade, id=unidade_id) if unidade_id else None

    if request.method == 'POST':
        unidade.delete()
        return redirect('unidade')
    return redirect('unidade_editar', unidade_id=unidade.id)


@user_passes_test(is_allowed)
@login_required
def curso(request):
    return render(request, 'interno/ver_cursos.html', {'cursos': Curso.objects.all()})

@never_cache
@ensure_csrf_cookie
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

@never_cache
@ensure_csrf_cookie
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

                    messages.success(request, 'Dados da curso atualizados com sucesso!')
                    return redirect('curso')
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

@never_cache
@ensure_csrf_cookie
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

@never_cache
@ensure_csrf_cookie
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

@never_cache
@ensure_csrf_cookie
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
                    return redirect('turma')
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

@never_cache
@ensure_csrf_cookie
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
    context = {
        'form': EmailForm(),
        'sorteio': sorteio_realizado()
    }

    return render(request, 'interno/controle.html', context)

@never_cache
@ensure_csrf_cookie
@user_passes_test(is_allowed)
@login_required
def controle_datetimes(request):
    controle = Controle.objects.first()

    context = {}

    if request.method == 'POST':
        form = ControleForm(request.POST, instance=controle)
        context.update({'form': form})

        if form.is_valid():
            try:
                print('saving')
                form.save()

            except IntegrityError as e:
                messages.error(request,f'Houve um problema com os dados inseridos. Contate a equipe de suporte.\n\nErro: {e}')
            except Exception as e:
                messages.error(request, f'Erro: {e}')
            else:
                return redirect('controle')

    else:
        form = ControleForm(instance=controle if controle else None)
        context.update({'form': form})

    return render(request, 'interno/controle_datetimes.html', context)

@never_cache
@ensure_csrf_cookie
def planilhas(request):
    context = {}

    if request.method == 'POST':
        form = EmailForm(request.POST)
        context.update({'form': form})
        if form.is_valid():
            try:
                email = form.cleaned_data['email']

                preparar_planilhas.delay(email)
            except IntegrityError as e:
                messages.error(request, f'Houve um problema com os dados inseridos. Contate a equipe de suporte.\n\nErro: {e}')

            except Exception as e:
                messages.error(request, f'Erro: {e}')
            else:
                context.update({'response': f'Planilhas enviadas com sucesso para {email}!'})
                context['form'] = EmailForm()

    return render(request, 'interno/controle.html', context)


@never_cache
@ensure_csrf_cookie
def logs(request):
    context = {}

    if request.method == 'POST':
        form = EmailForm(request.POST)
        context.update({'form': form})
        if form.is_valid():
            try:
                email = form.cleaned_data['email']

                preparar_log.delay(email)
            except IntegrityError as e:
                messages.error(request, f'Houve um problema com os dados inseridos. Contate a equipe de suporte.\n\nErro: {e}')

            except Exception as e:
                messages.error(request, f'Erro: {e}')
            else:
                context.update({'response': f'Log de registro enviado com sucesso para {email}!'})
                context['form'] = EmailForm()

    return render(request, 'interno/controle.html', context)


'''
    AUTENTICAÇÃO
'''
@never_cache
@ensure_csrf_cookie
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('estatisticas')
    else:
        form = LoginForm()
    return render(request, 'interno/accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@never_cache
@ensure_csrf_cookie
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'interno/accounts/register.html', {'form': form})

@never_cache
@ensure_csrf_cookie
def reset_password_view(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            users = User.objects.filter(email=email)
            if users.exists():
                for user in users:
                    subject = "Alteração de Senha"
                    content = render_to_string("emails/password_reset_email.html", {
                        "email": user.email,
                        'domain': get_current_site(request).domain,
                        'site_name': 'Incubadora de Robótica',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    })
                    enviar_emails.delay(
                        emails=[email],
                        content=content,
                        subject=subject,
                        has_html=True,
                    )
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
        if request.method == 'POST':
            form = CustomSetPasswordForm(user, request.POST)
            if form.is_valid():
                try:
                    form.save()
                except Exception as e:
                    print(e)
                return redirect('reset_password_complete')

        else:
            form = CustomSetPasswordForm(user)
        return render(request, 'interno/accounts/password_reset_confirm.html', {'form': form})
    else:
        return render(request, 'interno/accounts/password_reset_invalid.html')


def reset_password_complete_view(request):
    return render(request, 'interno/accounts/password_reset_complete.html')


def sorteio(request):
    agora = timezone.now()

    sortear.apply_async(eta=agora + timedelta(seconds=10))
    return redirect('estatisticas')
