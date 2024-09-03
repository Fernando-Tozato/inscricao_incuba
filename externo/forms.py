from django import forms

from incubadora.constants import *


class InscricaoForm(forms.Form):
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

    email = forms.EmailField(required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control',
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
