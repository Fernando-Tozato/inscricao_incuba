import os
from datetime import datetime

import django
from faker import Faker
from unidecode import unidecode

fake = Faker('pt_BR')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'incubadora.settings')
django.setup()

from database.models import Inscrito, Turma

# Definindo algumas constantes
INSCRITOS_POR_TURMA = 30

def generate_and_insert_data():
    turmas = Turma.objects.all()
    for turma in turmas:
        for i in range(INSCRITOS_POR_TURMA):
            nome = fake.name()
            nome_pesquisa = unidecode(nome).upper()
            nascimento = fake.date_of_birth(minimum_age=12, maximum_age=80)
            cpf = fake.cpf()
            filiacao = fake.name()
            escolaridade = fake.random_element(elements=('N_ALF', 'ALF', 'EF1_INC', 'EF1_COM', 'EF2_INC', 'EF2_COM',
                                                         'EM_INC', 'EM_COM', 'ES_INC', 'ES_COM', 'PG_COM'))
            email = None
            telefone = fake.phone_number() if fake.boolean(chance_of_getting_true=40) else None
            celular = fake.cellphone_number()
            cep = fake.postcode()
            rua = fake.street_name()
            numero = fake.building_number()
            bairro = fake.bairro()
            cidade = fake.city()
            uf = fake.estado_sigla()
            pcd = fake.boolean(chance_of_getting_true=15)
            ps = fake.boolean(chance_of_getting_true=15)

            nome_social = None
            nome_social_pesquisa = None
            if fake.boolean(chance_of_getting_true=20):
                nome_social = fake.name()
                nome_social_pesquisa = unidecode(nome_social).upper()

            rg = None
            data_emissao = None
            orgao_emissor = None
            uf_emissao = None
            if fake.boolean(chance_of_getting_true=80):
                rg = fake.rg()
                data_emissao = fake.date_between(start_date='-30y', end_date='-18y')
                orgao_emissor = fake.random_element(elements=('SSP', 'DETRAN', 'IFP', 'OAB'))
                uf_emissao = fake.estado_sigla()

            inscrito = Inscrito(
                nome=nome,
                nome_pesquisa=nome_pesquisa,
                nome_social=nome_social,
                nome_social_pesquisa=nome_social_pesquisa,
                nascimento=nascimento,
                cpf=cpf,
                rg=rg,
                data_emissao=data_emissao,
                orgao_emissor=orgao_emissor,
                uf_emissao=uf_emissao,
                filiacao=filiacao,
                escolaridade=escolaridade,
                email=email,
                telefone=telefone,
                celular=celular,
                cep=cep,
                rua=rua,
                numero=numero,
                complemento=None,
                bairro=bairro,
                cidade=cidade,
                uf=uf,
                pcd=pcd,
                ps=ps,
                id_turma=turma
            )

            try:
                inscrito.save()
            except Exception as e:
                print(e)
            else:
                print(i * int(turma.id))


if __name__ == '__main__':
    start = datetime.now()
    generate_and_insert_data()
    end = datetime.now()
    delta = end - start
    print(delta)
