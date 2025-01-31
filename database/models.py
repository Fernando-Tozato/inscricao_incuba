import hashlib
import re
import uuid
from datetime import datetime

from django.db import models
from unidecode import unidecode


class UfChoices(models.TextChoices):
    AC = 'AC'
    AL = 'AL'
    AP = 'AP'
    AM = 'AM'
    BA = 'BA'
    CE = 'CE'
    DF = 'DF'
    ES = 'ES'
    GO = 'GO'
    MA = 'MA'
    MT = 'MT'
    MS = 'MS'
    MG = 'MG'
    PA = 'PA'
    PB = 'PB'
    PR = 'PR'
    PE = 'PE'
    PI = 'PI'
    RJ = 'RJ'
    RN = 'RN'
    RS = 'RS'
    RO = 'RO'
    RR = 'RR'
    SC = 'SC'
    SP = 'SP'
    SE = 'SE'
    TO = 'TO'


class EscolaridadeChoices(models.TextChoices):
    N_ALF = 'N_ALF', 'Não Alfabetizado (a)'
    ALF = 'ALF', 'Alfabetizado (a)'
    EF1_INC = 'EF1_INC', 'Ensino Fundamental 1 Incompleto'
    EF1_COM = 'EF1_COM', 'Ensino Fundamental 1 Completo'
    EF2_INC = 'EF2_INC', 'Ensino Fundamental 2 Incompleto'
    EF2_COM = 'EF2_COM', 'Ensino Fundamental 2 Completo'
    EM_INC = 'EM_INC', 'Ensino Médio Incompleto'
    EM_COM = 'EM_COM', 'Ensino Médio Completo'
    ES_INC = 'ES_INC', 'Ensino Superior Incompleto'
    ES_COM = 'ES_COM', 'Ensino Superior Completo'
    PG_COM = 'PG_COM', 'Pós-Graduação Completa'


class Unidade(models.Model):
    nome = models.CharField(max_length=100)
    endereco1 = models.CharField(max_length=200)
    endereco2 = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.nome


class Curso(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    requisitos = models.TextField()
    imagem = models.ImageField(upload_to='cursos/', default='cursos/default.jpg', blank=True)
    unidades = models.ManyToManyField('Unidade')
    escolaridade = models.CharField(max_length=31, choices=EscolaridadeChoices.choices)
    idade = models.IntegerField()

    def __str__(self):
        return self.nome


class Turma(models.Model):
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE)
    dias = models.CharField(max_length=80)
    horario_entrada = models.TimeField()
    horario_saida = models.TimeField()
    vagas = models.IntegerField()
    professor = models.CharField(max_length=100)
    num_alunos = models.IntegerField(default=0)
    unidade = models.ForeignKey('Unidade', on_delete=models.CASCADE)
    
    def horario(self):
        return f'{self.horario_entrada.strftime("%H:%M")} - {self.horario_saida.strftime("%H:%M")}'
    
    def cotas(self):
        return (self.vagas * 30) // 100
    
    def ampla_conc(self):
        return self.vagas - self.cotas()

    def __str__(self):
        return f'{self.unidade.__str__()} - {self.curso.__str__()} - {self.dias} - {self.horario()}'


class Inscrito(models.Model):
    nome = models.CharField(max_length=100)
    nome_pesquisa = models.CharField(max_length=100) # nome do inscrito sem acentos e maiúsculo
    nome_social = models.CharField(max_length=100, null=True, default=None, blank=True)
    nome_social_pesquisa = models.CharField(max_length=100, null=True, default=None, blank=True) # nome social do inscrito sem acentos e maiúsculo
    nascimento = models.DateField()
    cpf = models.CharField(max_length=14, unique=True)
    rg = models.CharField(max_length=14, null=True, default=None, blank=True)
    data_emissao = models.DateField(null=True, default=None, blank=True)
    orgao_emissor = models.CharField(max_length=100, null=True, default=None, blank=True)
    uf_emissao = models.CharField(max_length=2, choices=UfChoices.choices, null=True, default=None, blank=True)
    filiacao = models.CharField(max_length=100)
    escolaridade = models.CharField(max_length=31, choices=EscolaridadeChoices.choices)
    email = models.EmailField(null=True, default=None, blank=True)
    telefone = models.CharField(max_length=14, null=True, default=None, blank=True)
    celular = models.CharField(max_length=16, null=True, default=None, blank=True)
    cep = models.CharField(max_length=10)
    rua = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, null=True, default=None, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    uf = models.CharField(max_length=2, choices=UfChoices.choices)
    pcd = models.BooleanField(default=False)
    ps = models.BooleanField(default=False)
    ja_sorteado = models.BooleanField(default=False) # inicialmente False, podendo ser alterado para True posteriormente
    id_turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    numero_inscricao = models.CharField(max_length=14, editable=False, unique=True) # gerado internamente em gerar_numero_inscricao(nome: str, cpf: str, nascimento: str) -> str
    data_inscricao = models.DateTimeField(auto_now_add=True)

    def dict_for_matricula(self):
        return {
            'nome': self.nome,
            'nome_social': self.nome_social,
            'nascimento': self.nascimento,
            'cpf': self.cpf,
            'rg': self.rg,
            'data_emissao': self.data_emissao,
            'orgao_emissor': self.orgao_emissor,
            'uf_emissao': self.uf_emissao,
            'filiacao': self.filiacao,
            'escolaridade': self.escolaridade,
            'email': self.email,
            'telefone': self.telefone,
            'celular': self.celular,
            'cep': self.cep,
            'rua': self.rua,
            'numero': self.numero,
            'complemento': self.complemento,
            'bairro': self.bairro,
            'cidade': self.cidade,
            'uf': self.uf,
            'pcd': self.pcd,
            'ps': self.ps,
            'id_turma': self.id_turma
        }

    def cpf_formatado(self):
        return f"{self.cpf[:3]}.{self.cpf[3:6]}.{self.cpf[6:9]}-{self.cpf[9:]}"

    def num_inscricao_formatado(self):
        return f"{self.numero_inscricao[:4]}.{self.numero_inscricao[4:8]}.{self.numero_inscricao[8:]}"

    def save(self, *args, **kwargs):
        self.nome_pesquisa = unidecode(self.nome.upper())
        self.nome_social_pesquisa = unidecode(self.nome_social.upper()) if self.nome_social else None
        self.cpf = re.sub(r'\D', '', self.cpf)
        if not self.numero_inscricao:
            self.numero_inscricao = self.gerar_numero_inscricao()
        super().save(*args, **kwargs)

    def gerar_numero_inscricao(self):
        salt = uuid.uuid4().hex
        nascimento = self.nascimento.strftime('%d/%m/%Y')
        return f'{self.gerar_hash(self.nome, salt)}{self.gerar_hash(self.cpf, salt)}{self.gerar_hash(nascimento, salt)}'

    def gerar_hash(self, dado, salt):
        codigo_hash = hashlib.sha256((str(dado)+salt).encode()).hexdigest()
        return f'{int(codigo_hash, 16) % 10000:04d}'

    def __str__(self):
        return f'{self.num_inscricao_formatado()}'


class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    nome_pesquisa = models.CharField(max_length=100) # nome do aluno sem acentos e maiúsculo
    nome_social = models.CharField(max_length=100, null=True, default=None, blank=True)
    nome_social_pesquisa = models.CharField(max_length=100, null=True, default=None, blank=True) # nome social do aluno sem acentos e maiúsculo
    nascimento = models.DateField()
    cpf = models.CharField(max_length=14, unique=True)
    rg = models.CharField(max_length=14, null=True, default=None, blank=True)
    data_emissao = models.DateField(null=True, default=None, blank=True)
    orgao_emissor = models.CharField(max_length=100, null=True, default=None, blank=True)
    uf_emissao = models.CharField(max_length=2, choices=UfChoices.choices, null=True, default=None, blank=True)
    filiacao = models.CharField(max_length=100)
    escolaridade = models.CharField(max_length=31, choices=EscolaridadeChoices.choices)
    email = models.EmailField(null=True, default=None, blank=True)
    telefone = models.CharField(max_length=14, null=True, default=None, blank=True)
    celular = models.CharField(max_length=16, null=True, default=None, blank=True)
    cep = models.CharField(max_length=10)
    rua = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, null=True, default=None, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    uf = models.CharField(max_length=2, choices=UfChoices.choices)
    pcd = models.BooleanField(default=False)
    ps = models.BooleanField(default=False)
    observacoes = models.TextField(null=True, default=None, blank=True)
    id_turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    data_matricula = models.DateTimeField(auto_now_add=True)

    def cpf_formatado(self):
        return f"{self.cpf[:3]}.{self.cpf[3:6]}.{self.cpf[6:9]}-{self.cpf[9:]}"

    def save(self, *args, **kwargs):
        self.nome_pesquisa = unidecode(self.nome.upper())
        self.nome_social_pesquisa = unidecode(self.nome_social.upper()) if self.nome_social else None
        self.cpf = re.sub(r'\D', '', self.cpf)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.cpf_formatado()}'


class Controle(models.Model):
    inscricao_inicio = models.DateTimeField()
    inscricao_fim = models.DateTimeField()
    sorteio_data = models.DateTimeField()
    matricula_sorte_inicio = models.DateTimeField()
    matricula_sorte_fim = models.DateTimeField()
    matricula_reman_inicio = models.DateTimeField()
    matricula_reman_fim = models.DateTimeField()
    aulas_inicio = models.DateTimeField()
    aulas_fim = models.DateTimeField()
