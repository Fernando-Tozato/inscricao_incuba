import os
import zipfile
from io import BytesIO

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.db.utils import IntegrityError
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from unidecode import unidecode

from database.models import *
from externo.forms import InscricaoForm, ResultadoForm
from externo.functions import *


def home(request):
    agora = timezone.now()
    controle = Controle.objects.first()
    inscricao_inicio = timezone.localtime(controle.inscricao_inicio)
    inscricao_fim = timezone.localtime(controle.inscricao_fim)
    vagas_disponiveis = timezone.localtime(controle.vagas_disponiveis)
    matricula_fim = timezone.localtime(controle.matricula_fim)

    context = {}

    if inscricao_inicio <= agora <= inscricao_fim:
        context.update({'inscricao': inscricao_fim})

    if vagas_disponiveis <= agora <= matricula_fim:
        context.update({'matricula_fim': matricula_fim})

    return render(request, 'externo/home.html', context)


def inscricao(request):
    turmas = get_turmas_as_json(['curso', 'dias', 'horario', 'idade', 'escolaridade'])
    context = {'turmas': turmas}

    if request.method == 'POST':
        form = InscricaoForm(request.POST)
        context.update({'form': form})
        if form.is_valid():
            nome = form.cleaned_data['nome']
            nome_pesquisa = unidecode(form.cleaned_data['nome'].upper())
            nome_social = form.cleaned_data['nome_social']
            nome_social_pesquisa = unidecode(form.cleaned_data['nome_social'].upper())
            nascimento = form.cleaned_data['nascimento']
            cpf = form.cleaned_data['cpf']
            rg = form.cleaned_data['rg']
            data_emissao = form.cleaned_data['data_emissao']
            orgao_emissor = form.cleaned_data['orgao_emissor']
            uf_emissao = form.cleaned_data['uf_emissao']
            filiacao = form.cleaned_data['filiacao']
            escolaridade = form.cleaned_data['escolaridade']
            email = form.cleaned_data['email']
            telefone = form.cleaned_data['telefone']
            celular = form.cleaned_data['celular']
            cep = form.cleaned_data['cep']
            rua = form.cleaned_data['rua']
            numero = form.cleaned_data['numero']
            complemento = form.cleaned_data['complemento']
            bairro = form.cleaned_data['bairro']
            cidade = form.cleaned_data['cidade']
            uf = form.cleaned_data['uf']
            pcd = form.cleaned_data['pcd']
            ps = form.cleaned_data['ps']
            curso = form.cleaned_data['curso']
            dias = form.cleaned_data['dias']
            horario = form.cleaned_data['horario']

            horario_entrada = horario[:5]
            horario_saida = horario[8:]

            id_turma = Turma.objects.filter(
                Q(curso=curso) &
                Q(dias=dias) &
                Q(horario_entrada=horario_entrada) &
                Q(horario_saida=horario_saida)
            )[0]

            numero_inscricao = gerar_numero_inscricao(nome, cpf, nascimento)

            inscrito = Inscrito(
                nome=nome,
                nome_pesquisa=nome_pesquisa,
                nome_social=nome_social if nome_social != '' else None,
                nome_social_pesquisa=nome_social_pesquisa if nome_social_pesquisa != '' else None,
                nascimento=datetime.datetime.strptime(nascimento, '%d/%m/%Y'),
                cpf=re.sub(r'\D', '', cpf),
                rg=rg if rg != '' else None,
                data_emissao=datetime.datetime.strptime(data_emissao, '%d/%m/%Y') if data_emissao != '' else None,
                orgao_emissor=orgao_emissor if orgao_emissor != '' else None,
                uf_emissao=uf_emissao if uf_emissao != '' else None,
                filiacao=filiacao,
                escolaridade=escolaridade,
                email=email if email != '' else None,
                telefone=telefone if telefone != '' else None,
                celular=celular if celular != '' else None,
                cep=cep,
                rua=rua,
                numero=numero,
                complemento=complemento if complemento != '' else None,
                bairro=bairro,
                cidade=cidade,
                uf=uf,
                pcd=pcd,
                ps=ps,
                ja_sorteado=False,
                id_turma=id_turma,
                numero_inscricao=numero_inscricao
            )

            try:
                inscrito.full_clean()
                inscrito.save()
            except ValidationError as e:
                messages.error(request, f'Candidato já inscrito.')
            except IntegrityError as e:
                messages.error(request, f'Houve um problema com os dados inseridos. Volte à página inicial, depois abra um formulário de inscrição em branco e preencha os campos novamente.')
            except Exception as e:
                messages.error(request, f'Erro: {e}')
            else:
                return render(request, 'externo/enviado_ext.html', {'inscricao': numero_inscricao})

    else:
        agora = timezone.now()
        controle = Controle.objects.first()
        inicio = timezone.localtime(controle.inscricao_inicio)
        fim = timezone.localtime(controle.inscricao_fim)
        remanescente = timezone.localtime(controle.matricula_geral)

        if agora < inicio:
            return render(request, 'externo/antes_inscricao.html', {'data': inicio})
        elif agora > fim:
            return render(request, 'externo/depois_inscricao.html', {'data_inscricao': fim, 'data_remanescente': remanescente})

        context.update({'form': InscricaoForm})

    return render(request, 'externo/inscricao.html', context)


def enviado(request):
    return render(request, 'externo/enviado_ext.html')


def editais(request):
    return render(request, 'externo/editais.html')


def resultado(request):
    turmas = get_turmas_as_json(['curso', 'dias', 'horario'])
    context = {'turmas': turmas}

    if request.method == 'POST':
        form = ResultadoForm(request.POST)
        context.update({'form': form})
        if form.is_valid():
            curso = form.cleaned_data['curso']
            dias = form.cleaned_data['dias']
            horario = form.cleaned_data['horario']

            horario_entrada = horario[:5]
            horario_saida = horario[8:]

            id_turma = Turma.objects.filter(
                Q(curso=curso) &
                Q(dias=dias) &
                Q(horario_entrada=horario_entrada) &
                Q(horario_saida=horario_saida)
            )[0]

            sorteados = Inscrito.objects.filter(Q(id_turma=id_turma) & Q(ja_sorteado=True))
            if len(sorteados) == 0:
                context.update({'sorteados': -1})
            else:
                context.update({'sorteados':sorteados})

    else:
        agora = timezone.now()
        controle = Controle.objects.first()
        sorteio = timezone.localtime(controle.sorteio_data)  # type: ignore

        if agora < sorteio:
            return render(request, 'externo/antes_resultado.html', {'data': sorteio})

        context.update({'form': ResultadoForm})

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
