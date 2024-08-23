import json
import os
import zipfile
from io import BytesIO

from unidecode import unidecode
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.db.utils import IntegrityError
from django.http import HttpResponse, Http404
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect

from database.models import *
from externo.forms import InscricaoForm
from externo.functions import get_turmas_as_json


def home(request):
    return render(request, 'externo/home.html')


def inscricao(request):
    turmas = get_turmas_as_json(['curso', 'dias', 'horario', 'idade', 'escolaridade'])
    context = {'turmas': turmas}

    if request.method == 'POST':
        form = InscricaoForm(request.POST)
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

            print(f'{horario}\n{horario_entrada}\n{horario_saida}')

            id_turma = Turma.objects.filter(
                Q(curso=curso) &
                Q(dias=dias) &
                Q(horario_entrada=horario_entrada) &
                Q(horario_saida=horario_saida)
            )

            inscrito = Inscrito(
                nome=nome,
                nome_pesquisa=nome_pesquisa,
                nome_social=nome_social if nome_social != '' else None,
                nome_social_pesquisa=nome_social_pesquisa if nome_social_pesquisa != '' else None,
                nascimento=nascimento,
                cpf=cpf,
                rg=rg if rg != '' else None,
                data_emissao=data_emissao if data_emissao != '' else None,
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
                id_turma=id_turma
            )

            try:
                inscrito.full_clean()
                inscrito.save()
            except ValidationError as e:
                return JsonResponse({'error': e}, status=400)
            except IntegrityError as e:
                return JsonResponse({'error': e}, status=400)
            except Exception as e:
                return JsonResponse({'error': e}, status=400)
            finally:
                return redirect('enviado')

        else:
            context.update({'form': form})

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
            pcd = data['pcd']
            ps = data['ps']
            id_turma = get_object_or_404(Turma, id=data['id_turma'])

            print(pcd, type(pcd))
            print(ps, type(ps))

            inscrito = Inscrito(
                nome=nome,
                nome_pesquisa=nome_pesquisa,
                nome_social=nome_social if nome_social != '' else None,
                nome_social_pesquisa=nome_social_pesquisa if nome_social_pesquisa != '' else None,
                nascimento=nascimento,
                cpf=cpf,
                rg=rg if rg != '' else None,
                data_emissao=data_emissao if data_emissao != '' else None,
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
                id_turma=id_turma
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
    return render(request, 'externo/editais.html')


def resultado(request):
    agora = timezone.now()
    controle = Controle.objects.first()
    sorteio = timezone.localtime(controle.sorteio_data)  # type: ignore

    if agora < sorteio:
        return render(request, 'externo/antes_resultado.html', {'data': sorteio})

    cursos = Turma.objects.values_list('curso', flat=True).distinct()
    return render(request, 'externo/resultado.html', {'cursos': cursos})


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
