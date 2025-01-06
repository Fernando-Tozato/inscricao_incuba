import datetime
import re

from django.db.models import Q
from unidecode import unidecode

from database.models import Turma, Aluno, Inscrito
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
    else:
        curso = form.cleaned_data['curso']
        professor = form.cleaned_data['professor']
        dias = form.cleaned_data['dias']
        horario_entrada = form.cleaned_data['horario_entrada']
        horario_saida = form.cleaned_data['horario_saida']
        vagas = form.cleaned_data['vagas']
        idade = form.cleaned_data['idade']
        escolaridade = form.cleaned_data['escolaridade']

        print(horario_entrada, horario_saida)
        print(type(horario_entrada), type(horario_saida))

        turma = Turma(
            curso=curso,
            professor=professor,
            dias=dias,
            horario_entrada=horario_entrada,
            horario_saida=horario_saida,
            vagas=vagas,
            idade=idade,
            escolaridade=escolaridade
        )

        return turma
