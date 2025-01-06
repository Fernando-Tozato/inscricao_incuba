import datetime
import json
import re

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models import Q, QuerySet
from unidecode import unidecode

from database.models import Turma, Aluno, Inscrito, Curso, Unidade
from externo.functions import gerar_numero_inscricao

def get_turma_from_form(form):
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

    return id_turma

def load_form_to_object(form, obj):
    if type(obj) in [Aluno, Inscrito]:
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

        id_turma = get_turma_from_form(form)

        if type(obj) == Aluno:
            observacoes = form.cleaned_data['observacoes']

            aluno = Aluno(
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
                observacoes=observacoes if observacoes != '' else None,
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
                id_turma=id_turma
            )
            return aluno
        else:
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
                id_turma=id_turma,
                numero_inscricao=numero_inscricao
            )
            return inscrito

    elif type(obj) == Turma:
        curso = form.cleaned_data['curso']
        dias = form.cleaned_data['dias']
        horario_entrada = form.cleaned_data['horario_entrada']
        horario_saida = form.cleaned_data['horario_saida']
        vagas = form.cleaned_data['vagas']
        professor = form.cleaned_data['professor']
        unidade = form.cleaned_data['unidade']

        print(horario_entrada, horario_saida)
        print(type(horario_entrada), type(horario_saida))

        turma = Turma(
            curso=curso,
            dias=dias,
            horario_entrada=horario_entrada,
            horario_saida=horario_saida,
            vagas=vagas,
            professor=professor,
            unidade=unidade
        )

        return turma

    elif type(obj) == Curso:
        nome = form.cleaned_data['nome']
        descricao = form.cleaned_data['descricao']
        requisitos = form.cleaned_data['requisitos']
        image = form.cleaned_data['image']
        unidades = form.cleaned_data['unidades']
        escolaridade = form.cleaned_data['escolaridade']
        idade = form.cleaned_data['idade']

        curso = Curso(
            nome=nome,
            descricao=descricao,
            requisitos=requisitos,
            image=image,
            unidades=unidades,
            escolaridade=escolaridade,
            idade=idade
        )

        return curso

    elif type(obj) == Unidade:
        nome = form.cleaned_data['nome']
        endereco1 = form.cleaned_data['endereco1']
        endereco2 = form.cleaned_data['endereco2']

        unidade = Unidade(
            nome=nome,
            endereco1=endereco1,
            endereco2=endereco2
        )

        return unidade

def get_unidade_as_json():
    unidades: QuerySet[Unidade] = Unidade.objects.all()
    unidades_list: list[dict] = []

    campos = ['nome', 'endereco1', 'endereco2']

    for unidade in unidades:
        turma_dict: dict[str: str | int] = {}

        for campo in campos:
            if hasattr(unidade, campo):
                valor = getattr(unidade, campo)
                if callable(valor):  # Se o atributo for um método, chama-o
                    valor = valor() # Formatação para campos de horário
                turma_dict[campo] = valor

        unidades_list.append(turma_dict)

    return json.dumps(unidades_list, cls=DjangoJSONEncoder)

def get_curso_as_json():
    cursos: QuerySet[Curso] = Curso.objects.all()
    cursos_list: list[dict] = []

    campos = ['nome', 'descricao', 'requisitos', 'imagem', 'unidades', 'escolaridade', 'idade']

    for curso in cursos:
        turma_dict: dict[str: str | int] = {}

        for campo in campos:
            if hasattr(curso, campo):
                valor = getattr(curso, campo)
                turma_dict[campo] = valor

        cursos_list.append(turma_dict)

    return json.dumps(cursos_list, cls=DjangoJSONEncoder)