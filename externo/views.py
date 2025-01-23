import os
import zipfile
from io import BytesIO

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.db.utils import IntegrityError
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from database.models import *
from externo.forms import InscricaoForm, ResultadoForm
from externo.functions import *


def home(request):
    context = {}

    agora = timezone.localtime(timezone.now())
    controle = Controle.objects.first()
    if controle:
        inscricao_inicio = timezone.localtime(controle.inscricao_inicio)
        inscricao_fim = timezone.localtime(controle.inscricao_fim)
        matricula_sorte_inicio = timezone.localtime(controle.matricula_sorte_inicio)
        matricula_sorte_fim = timezone.localtime(controle.matricula_sorte_fim)
        matricula_reman_inicio = timezone.localtime(controle.matricula_reman_inicio)
        matricula_reman_fim = timezone.localtime(controle.matricula_reman_fim)

        if inscricao_inicio <= agora <= inscricao_fim:
            context.update({'inscricao': {
                'inscricao_inicio': inscricao_inicio,
                'inscricao_fim': inscricao_fim,
            }})

        if matricula_sorte_inicio <= agora <= matricula_reman_fim:
            context.update({'matricula': {
                'matricula_sorte_inicio': matricula_sorte_inicio,
                'matricula_sorte_fim': matricula_sorte_fim,
                'matricula_reman_inicio': matricula_reman_inicio,
                'matricula_reman_fim': matricula_reman_fim,
            }})

        if agora > matricula_reman_fim:
            context.update({'fim': True})

    return render(request, 'externo/home.html', context)


def inscricao(request):
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

    if request.method == 'POST':
        form = InscricaoForm(request.POST)
        context.update({'form': form})
        if form.is_valid():

            try:
                inscrito: Inscrito = form.save()
            except ValidationError as e:
                messages.error(request, f'Candidato já inscrito.')
            except IntegrityError as e:
                messages.error(request, f'Houve um problema com os dados inseridos. Volte à página inicial, depois abra um formulário de inscrição em branco e preencha os campos novamente.')
            except Exception as e:
                messages.error(request, f'Erro: {e}')
            else:
                return render(request, 'externo/enviado_ext.html', {'inscricao': inscrito.num_inscricao_formatado()})

    else:
        agora = timezone.now()
        controle = Controle.objects.first()
        if controle:
            inicio = timezone.localtime(controle.inscricao_inicio)
            fim = timezone.localtime(controle.inscricao_fim)
            matricula_inicio = timezone.localtime(controle.matricula_reman_inicio)
            matricula_fim = timezone.localtime(controle.matricula_reman_fim)

            if agora < inicio:
                return render(request, 'externo/antes_inscricao.html', {'data': inicio})
            elif agora > fim:
                return render(request, 'externo/depois_inscricao.html', {'data_inscricao': fim, 'matricula_inicio': matricula_inicio, 'matricula_fim': matricula_fim})

        context.update({'form': InscricaoForm})

    return render(request, 'externo/inscricao.html', context)


def enviado(request):
    return render(request, 'externo/enviado_ext.html')


def editais(request):
    return render(request, 'externo/editais.html')


def resultado(request, turma_id=None):
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

    turma = get_object_or_404(Turma, id=turma_id) if turma_id else None

    if turma:
        sorteados = Inscrito.objects.filter(Q(id_turma=turma) & Q(ja_sorteado=True))
        context.update({'sorteados': sorteados})

    if request.method == 'POST':
        form = ResultadoForm(request.POST, turma=turma)
        context.update({'form': form})
        if form.is_valid():
            id_turma = form.cleaned_data['id_turma']

            return redirect('resultado_id', turma_id=int(id_turma.id))

    else:
        agora = timezone.now()
        controle = Controle.objects.first()
        sorteio = timezone.localtime(controle.sorteio_data)  # type: ignore

        if agora < sorteio:
            return render(request, 'externo/antes_resultado.html', {'data': sorteio})

        context.update({'form': ResultadoForm(turma=turma)})

    return render(request, 'externo/resultado.html', context)


def resultado_id(request, id_turma):
    agora = timezone.now()
    controle = Controle.objects.first()
    sorteio = timezone.localtime(controle.sorteio_data)  # type: ignore

    if agora < sorteio:
        return render(request, 'externo/antes_resultado.html', {'data': sorteio})

    cursos = Turma.objects.values_list('curso', flat=True).distinct()
    turma = get_object_or_404(Turma, id=id_turma)
    sorteados = Inscrito.objects.filter(Q(id_turma=turma) & Q(ja_sorteado=True))

    busca = {
        'curso': turma.curso,
        'dias': turma.dias,
        'horario': turma.horario()
    }

    if len(sorteados) == 0:
        sorteados = -1

    return render(request, 'externo/resultado.html',
                  {'cursos': cursos, 'sorteados': sorteados, 'busca': json.dumps(busca)})


def design(request):
    return render(request, 'externo/cursos/design.html')


def educacao(request):
    return render(request, 'externo/cursos/educacao.html')


def excel(request):
    return render(request, 'externo/cursos/excel.html')


def gestao(request):
    return render(request, 'externo/cursos/gestao.html')


def info_basica(request):
    return render(request, 'externo/cursos/info_basica.html')


def info_melhor_idade(request):
    return render(request, 'externo/cursos/info_melhor_idade.html')


def marketing_digital(request):
    return render(request, 'externo/cursos/marketing_digital.html')


def marketing_emp(request):
    return render(request, 'externo/cursos/marketing_emp.html')


def montagem(request):
    return render(request, 'externo/cursos/montagem.html')


def robotica(request):
    return render(request, 'externo/cursos/robotica.html')


def download_validadores(request):
    planilhas_dir = os.path.join(settings.MEDIA_ROOT, 'sorteio')

    # Verificar se a pasta "planilhas" existe
    if not os.path.exists(planilhas_dir):
        raise Http404("A pasta 'planilhas' não foi encontrada")

    # Listar todos os arquivos dentro da pasta "planilhas"
    filenames = os.listdir(planilhas_dir)

    zip_subdir = "validadores"
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


def download_1(request):
    planilhas_dir = os.path.join(settings.MEDIA_ROOT, 'edital_2024_1')

    # Verificar se a pasta "planilhas" existe
    if not os.path.exists(planilhas_dir):
        raise Http404("A pasta 'planilhas' não foi encontrada")

    # Listar todos os arquivos dentro da pasta "planilhas"
    filenames = os.listdir(planilhas_dir)

    zip_subdir = "edital_e_anexos_2024_1"
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


def download_2(request):
    planilhas_dir = os.path.join(settings.MEDIA_ROOT, 'edital_2024_2')

    # Verificar se a pasta "planilhas" existe
    if not os.path.exists(planilhas_dir):
        raise Http404("A pasta 'planilhas' não foi encontrada")

    # Listar todos os arquivos dentro da pasta "planilhas"
    filenames = os.listdir(planilhas_dir)

    zip_subdir = "edital_e_anexos_2024_2"
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
