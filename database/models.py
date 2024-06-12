from django.db import models
import random, hashlib, string

class Turma(models.Model):
    curso = models.CharField(max_length=100)
    dias = models.CharField(max_length=20)
    horario_entrada = models.TimeField()
    horario_saida = models.TimeField()
    vagas = models.IntegerField()
    escolaridade = models.IntegerField()
    idade = models.IntegerField()
    professor = models.CharField(max_length=100)
    
    def horario(self):
        return f'{self.horario_entrada.strftime('%H:%M')} - {self.horario_saida.strftime('%H:%M')}'

class Inscrito(models.Model):
    nome = models.CharField(max_length=100)
    nome_pesquisa = models.CharField(max_length=100)
    nome_social = models.CharField(max_length=100, null=True, default=None, blank=True)
    nome_social_pesquisa = models.CharField(max_length=100, null=True, default=None, blank=True)
    nascimento = models.DateField()
    cpf = models.CharField(max_length=14, unique=True)
    rg = models.CharField(max_length=14, null=True, default=None, blank=True)
    data_emissao = models.DateField(null=True, default=None, blank=True)
    orgao_emissor = models.CharField(max_length=100, null=True, default=None, blank=True)
    uf_emissao = models.CharField(max_length=2, null=True, default=None, blank=True)
    filiacao = models.CharField(max_length=100)
    escolaridade = models.IntegerField()
    email = models.EmailField(null=True, default=None, blank=True)
    telefone = models.CharField(max_length=14, null=True, default=None, blank=True)
    celular = models.CharField(max_length=16, null=True, default=None, blank=True)
    cep = models.CharField(max_length=10)
    rua = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, null=True, default=None, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)
    id_turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    
    def hash(self):
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_and_digits) for i in range(64))

class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    nome_pesquisa = models.CharField(max_length=100)
    nome_social = models.CharField(max_length=100, null=True, default=None, blank=True)
    nome_social_pesquisa = models.CharField(max_length=100, null=True, default=None, blank=True)
    nascimento = models.DateField()
    cpf = models.CharField(max_length=14, unique=True)
    rg = models.CharField(max_length=14, null=True, default=None, blank=True)
    data_emissao = models.DateField()
    orgao_emissor = models.CharField(max_length=100)
    uf_emissao = models.CharField(max_length=2)
    filiacao = models.CharField(max_length=100)
    escolaridade = models.IntegerField()
    email = models.EmailField(null=True, default=None, blank=True)
    telefone = models.CharField(max_length=14, null=True, default=None, blank=True)
    celular = models.CharField(max_length=16, null=True, default=None, blank=True)
    cep = models.CharField(max_length=10)
    rua = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, null=True, default=None, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)
    id_turma = models.ForeignKey(Turma, on_delete=models.CASCADE)

class Sorteado(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    id_inscrito = models.OneToOneField(Inscrito, on_delete=models.CASCADE)
    id_turma = models.ForeignKey(Turma, on_delete=models.CASCADE)