from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User

from database.models import Inscrito, Turma
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


class TurmaForm(forms.Form):
    curso = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control required',
                                                         'placeholder': 'Curso'}))

    professor = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control required',
                                                         'placeholder': 'Professor'}))

    dias = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control required',
                                                         'placeholder': 'Dias da semana'}))

    horario_entrada = forms.TimeField(widget=forms.TimeInput(format='%H:%M',
                                                             attrs={'class': 'form-control required',
                                                                    'placeholder': 'Horário entrada'}))

    horario_saida = forms.TimeField(widget=forms.TimeInput(format='%H:%M',
                                                           attrs={'class': 'form-control required',
                                                                  'placeholder': 'Horário saída'}))

    vagas = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control required',
                                                             'placeholder': 'Vagas'}))

    idade = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control required',
                                                             'placeholder': 'Idade'}))

    escolaridade = forms.ChoiceField(choices=ESCOLARIDADE_OPTIONS,
                                     widget=forms.Select(attrs={'class': 'form-select required'}),
                                     initial='')

    is_blank = True

    def __init__(self, *args, **kwargs):
        turma: Turma | None = kwargs.pop('turma', None)
        super(TurmaForm, self).__init__(*args, **kwargs)

        if turma is not None:
            self.fields['curso'].initial = turma.curso
            self.fields['professor'].initial = turma.professor
            self.fields['dias'].initial = turma.dias
            self.fields['vagas'].initial = turma.vagas
            self.fields['idade'].initial = turma.idade
            self.fields['escolaridade'].initial = turma.escolaridade
            self.is_blank = False
