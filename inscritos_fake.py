from datetime import datetime
import random, django, os
from faker import Faker
from cpf_generator import CPF  # Certifique-se de ter instalado este pacote
  # Substitua 'seu_app' pelo nome da sua aplicação Django
from django.shortcuts import get_object_or_404

fake = Faker('pt_BR')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'incubadora.settings')
django.setup()

from database.models import Inscrito, Turma

# Função para converter string para data
def str_to_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d').date()

# Definindo algumas constantes
NUM_TURMAS = 64
INSCRITOS_POR_TURMA = 100

# Função para gerar dados aleatórios e inserir no banco de dados
def generate_and_insert_data():
    for id_turma in range(1, NUM_TURMAS + 1):
        for _ in range(INSCRITOS_POR_TURMA):
            # Gerando dados aleatórios
            nome = fake.name()
            nome_pesquisa = nome.upper()
            nascimento = fake.date_of_birth(minimum_age=12, maximum_age=80)
            cpf = CPF.generate()
            filiacao = fake.name()
            escolaridade = random.randint(2, 7)
            email = fake.email()
            telefone = fake.phone_number()
            celular = fake.cellphone_number()
            cep = fake.postcode()
            rua = fake.street_name()
            numero = fake.building_number()
            bairro = fake.neighborhood()
            cidade = fake.city()
            uf = fake.random_element(elements=('RJ', 'SP', 'MG', 'RS', 'PR'))
            pcd = fake.boolean(chance_of_getting_true=20)
            ps = fake.boolean(chance_of_getting_true=10)
            
            # Gerar dados opcionais
            nome_social = None
            nome_social_pesquisa = None
            if fake.boolean(chance_of_getting_true=20):
                nome_social = fake.name()
                nome_social_pesquisa = nome_social.upper()

            rg = None
            data_emissao = None
            orgao_emissor = None
            uf_emissao = None
            if fake.boolean(chance_of_getting_true=80):
                rg = fake.random_number(digits=9, fix_len=True)
                data_emissao = fake.date_between(start_date='-30y', end_date='-18y')
                orgao_emissor = fake.random_element(elements=('SSP', 'DETRAN', 'IFP', 'OAB'))
                uf_emissao = fake.random_element(elements=('RJ', 'SP', 'MG', 'RS', 'PR'))
            
            turma = get_object_or_404(Turma, id=id_turma)
            
            # Inserir no banco de dados
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
                bairro=bairro,
                cidade=cidade,
                uf=uf,
                pcd=pcd,
                ps=ps,
                id_turma=turma
            )
            inscrito.save()

if __name__ == '__main__':
    generate_and_insert_data()
