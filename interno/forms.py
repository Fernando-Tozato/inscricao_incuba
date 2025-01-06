from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User

from database.models import Inscrito, Turma, Curso, Unidade
from incubadora.constants import *


class MatriculaForm(forms.Form):
    nome = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control required',
                                                         'placeholder': 'Nome'}))
    nome_social = forms.CharField(required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': 'Nome social'}))
    nascimento = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control required',
                                                               'placeholder': 'Nascimento'}))
    cpf = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control required',
                                                        'placeholder': 'CPF'}))
    rg = forms.CharField(required=False,
                         widget=forms.TextInput(attrs={'class': 'form-control',
                                                       'placeholder': 'RG'}))
    data_emissao = forms.CharField(required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Emissão'}))
    orgao_emissor = forms.CharField(required=False,
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Emissor'}))
    uf_emissao = forms.ChoiceField(choices=UF_OPTIONS,
                                   required=False,
                                   widget=forms.Select(attrs={'class': 'form-select'}),
                                   initial='')
    filiacao = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control required',
                                                             'placeholder': 'Filiação'}))
    escolaridade = forms.ChoiceField(choices=ESCOLARIDADE_OPTIONS,
                                     widget=forms.Select(attrs={'class': 'form-select required'}),
                                     initial='')
    pcd = forms.BooleanField(required=False,
                             widget=forms.CheckboxInput(attrs={'class': 'form-check-input required',
                                                               'role': 'switch'}))
    ps = forms.BooleanField(required=False,
                            widget=forms.CheckboxInput(attrs={'class': 'form-check-input required',
                                                              'role': 'switch'}))
    observacoes = forms.CharField(required=False,
                                  widget=forms.Textarea(attrs={'class': 'form-control',
                                                               'style': 'height: 5rem;',
                                                               'placeholder': 'Observações'}))

    email = forms.EmailField(required=False,
                             widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'placeholder': 'Email'}))
    telefone = forms.CharField(required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Telefone'}))
    celular = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control required',
                                                            'placeholder': 'Celular'}))

    cep = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control required',
                                                        'placeholder': 'CEP'}))
    rua = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control required',
                                                        'placeholder': 'Rua'}))
    numero = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control required',
                                                           'placeholder': 'Número'}))
    complemento = forms.CharField(required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': 'Complemento'}))
    bairro = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control required',
                                                           'placeholder': 'Bairro'}))
    cidade = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control required',
                                                           'placeholder': 'Cidade'}))
    uf = forms.ChoiceField(choices=UF_OPTIONS,
                           widget=forms.Select(attrs={'class': 'form-select required'}),
                           initial='')

    curso = forms.CharField(widget=forms.Select(choices=[('', 'Selecione...')],
                                                attrs={'class': 'form-select required',
                                                       'disabled': 'true'}))
    dias = forms.CharField(widget=forms.Select(choices=[('', 'Selecione...')],
                                               attrs={'class': 'form-select required',
                                                      'disabled': 'true'}))
    horario = forms.CharField(widget=forms.Select(choices=[('', 'Selecione...')],
                                                  attrs={'class': 'form-select required',
                                                         'disabled': 'true'}))

    turma = forms.CharField(required=False,
                            widget=forms.TextInput(attrs={'class': 'd-none'}))

    def __init__(self, *args, **kwargs):
        inscrito: Inscrito | None = kwargs.pop('inscrito', None)
        super(MatriculaForm, self).__init__(*args, **kwargs)

        if inscrito is not None:
            self.fields['nome'].initial = inscrito.nome
            self.fields['nome_social'].initial = inscrito.nome_social
            self.fields['nascimento'].initial = inscrito.nascimento.strftime('%d/%m/%Y')
            self.fields['cpf'].initial = inscrito.cpf
            self.fields['rg'].initial = inscrito.rg
            self.fields['data_emissao'].initial = inscrito.data_emissao.strftime('%d/%m/%Y') if inscrito.data_emissao is not None else None
            self.fields['orgao_emissor'].initial = inscrito.orgao_emissor
            self.fields['uf_emissao'].initial = inscrito.uf_emissao
            self.fields['filiacao'].initial = inscrito.filiacao
            self.fields['escolaridade'].initial = inscrito.escolaridade
            self.fields['pcd'].initial = inscrito.pcd
            self.fields['ps'].initial = inscrito.ps
            self.fields['email'].initial = inscrito.email
            self.fields['telefone'].initial = inscrito.telefone
            self.fields['celular'].initial = inscrito.celular
            self.fields['cep'].initial = inscrito.cep
            self.fields['rua'].initial = inscrito.rua
            self.fields['numero'].initial = inscrito.numero
            self.fields['complemento'].initial = inscrito.complemento
            self.fields['bairro'].initial = inscrito.bairro
            self.fields['cidade'].initial = inscrito.cidade
            self.fields['uf'].initial = inscrito.uf
            self.fields['turma'].initial = inscrito.id_turma.pk


class BuscaForm(forms.Form):
    busca = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': 'Busca'}))


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField()


class CustomSetPasswordForm(SetPasswordForm):
    senha = forms.CharField(widget=forms.PasswordInput)
    confirmacao_senha = forms.CharField(widget=forms.PasswordInput)


class UnidadeForm(forms.Form):
    nome = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control required',
                                                         'placeholder': 'Nome'}))

    endereco1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control required',
                                                              'placeholder': 'Endereço principal'}))

    endereco2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': 'Endereço secundário'}))

    is_blank = True

    def __init__(self, *args, **kwargs):
        unidade: Unidade | None = kwargs.pop('unidade', None)
        super(UnidadeForm, self).__init__(*args, **kwargs)

        if unidade is not None:
            self.id_unidade = unidade.id
            self.fields['nome'].initial = unidade.nome
            self.fields['endereco1'].initial = unidade.endereco1
            self.fields['endereco2'].initial = unidade.endereco2
            self.is_blank = False


class CursoForm(forms.Form):
    nome = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control required',
                                                         'placeholder': 'Nome'}))

    descricao = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control required',
                                                             'placeholder': 'Descrição'}))

    requisitos = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control required',
                                                              'placeholder': 'Requisitos'}))

    imagem = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control',
                                                           'placeholder': 'Imagem'}))

    unidades = forms.ModelMultipleChoiceField(queryset=Unidade.objects.all(),
                                              widget=forms.SelectMultiple(attrs={'class': 'form-select required'}),
                                              required=True,
                                              label='Unidades disponíveis')

    escolaridade = forms.ChoiceField(choices=ESCOLARIDADE_OPTIONS,
                                     widget=forms.Select(attrs={'class': 'form-select required'}),
                                     initial='')

    idade = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control required',
                                                             'placeholder': 'Idade'}))

    is_blank = True

    def __init__(self, *args, **kwargs):
        curso: Curso | None = kwargs.pop('curso', None)
        super(CursoForm, self).__init__(*args, **kwargs)

        if curso is not None:
            self.id_turma = curso.id
            self.fields['nome'].initial = curso.nome
            self.fields['descricao'].initial = curso.descricao
            self.fields['requisitos'].initial = curso.requisitos
            self.fields['imagem'].initial = curso.imagem
            self.fields['unidades'].initial = curso.unidades
            self.fields['escolaridade'].initial = curso.escolaridade
            self.fields['idade'].initial = curso.idade
            self.is_blank = False


class TurmaForm(forms.Form):
    curso = forms.ModelChoiceField(queryset=Curso.objects.all(),
                                   widget=forms.Select(attrs={'class': 'form-select required',
                                                              'placeholder': 'Curso'}))

    dias = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control required',
                                                         'placeholder': 'Dias da semana'}))

    horario_entrada = forms.TimeField(widget=forms.TimeInput(format='%H:%M',
                                                             attrs={'class': 'form-control required',
                                                                    'placeholder': 'Horário entrada',
                                                                    'type': 'time'}))

    horario_saida = forms.TimeField(widget=forms.TimeInput(format='%H:%M',
                                                           attrs={'class': 'form-control required',
                                                                  'placeholder': 'Horário saída',
                                                                  'type': 'time'}))

    vagas = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control required',
                                                             'placeholder': 'Vagas'}))

    professor = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control required',
                                                              'placeholder': 'Professor'}))

    unidade = forms.CharField(widget=forms.Select(choices=[('', 'Selecione...')],
                                                  attrs={'class': 'form-select required',
                                                         'disabled': 'true'}))

    is_blank = True

    def __init__(self, *args, **kwargs):
        turma: Turma | None = kwargs.pop('turma', None)
        super(TurmaForm, self).__init__(*args, **kwargs)

        if turma is not None:
            self.id_turma = turma.id
            self.fields['curso'].initial = turma.curso
            self.fields['dias'].initial = turma.dias
            self.fields['horario_entrada'].initial = turma.horario_entrada
            self.fields['horario_saida'].initial = turma.horario_saida
            self.fields['vagas'].initial = turma.vagas
            self.fields['professor'].initial = turma.professor
            self.fields['unidade'].initial = turma.unidade
            self.is_blank = False
