from django.db import models

class Turmas(models.Model):
    curso = models.CharField(max_length=100)
    dias = models.CharField(max_length=20)
    horario = models.TimeField()

class Contatos(models.Model):
    email = models.EmailField()
    telefone = models.CharField(max_length=10)
    celular = models.CharField(max_length=11)

class Enderecos(models.Model):
    cep = models.CharField(max_length=8)
    rua = models.CharField(max_length=100)
    numero = models.IntegerField()
    complemento = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)

class Alunos(models.Model):
    nome = models.CharField(max_length=100)
    nascimento = models.DateField()
    cpf = models.CharField(max_length=11)
    rg = models.CharField(max_length=9)
    data_emissao = models.DateField()
    orgao_emissor = models.CharField(max_length=100)
    uf_emissao = models.CharField(max_length=2)
    nome_mae = models.CharField(max_length=100)
    nasc_mae = models.DateField()
    nome_pai = models.CharField(max_length=100)
    nasc_pai = models.DateField()
    nivel_escola = models.CharField(max_length=24)
    instituicao = models.CharField(max_length=100)
    id_contato = models.OneToOneField(Contatos, on_delete=models.CASCADE)
    id_endereco = models.OneToOneField(Enderecos, on_delete=models.CASCADE)
    id_turma = models.ForeignKey(Turmas, on_delete=models.CASCADE)