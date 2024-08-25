from django import forms

UF_options = [
    ('', 'Selecione...'),
    ('AC', 'AC'),
    ('AL', 'AL'),
    ('AP', 'AP'),
    ('AM', 'AM'),
    ('BA', 'BA'),
    ('CE', 'CE'),
    ('DF', 'DF'),
    ('ES', 'ES'),
    ('GO', 'GO'),
    ('MA', 'MA'),
    ('MT', 'MT'),
    ('MS', 'MS'),
    ('MG', 'MG'),
    ('PA', 'PA'),
    ('PB', 'PB'),
    ('PR', 'PR'),
    ('PE', 'PE'),
    ('PI', 'PI'),
    ('RJ', 'RJ'),
    ('RN', 'RN'),
    ('RS', 'RS'),
    ('RO', 'RO'),
    ('RR', 'RR'),
    ('SC', 'SC'),
    ('SP', 'SP'),
    ('SE', 'SE'),
    ('TO', 'TO')
]

escolaridade_options = [
    ('', 'Selecione...'),
    ('1', 'Não Alfabetizado'),
    ('2', 'Alfabetização'),
    ('3', 'Ensino Fundamental 1 Incompleto'),
    ('4', 'Ensino Fundamental 1 Completo'),
    ('5', 'Ensino Fundamental 2 Incompleto'),
    ('6', 'Ensino Fundamental 2 Completo'),
    ('7', 'Ensino Médio Incompleto'),
    ('8', 'Ensino Médio Completo'),
    ('9', 'Ensino Superior Incompleto'),
    ('10', 'Ensino Superior Completo'),
    ('11', 'Pós-graduação Completa')
]


class InscricaoForm(forms.Form):
    nome = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control required',
                                                         'placeholder': 'Nome'}))
    nome_social = forms.CharField(required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': 'Nome social'}))
    nascimento = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control required',
                                                               'placeholder': 'Nascimento'}))
    cpf = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control required',
                                                        'placeholder': 'CPF'}))
    rg = forms.CharField(required=False,
                         widget=forms.TextInput(attrs={'class': 'form-control',
                                                       'placeholder': 'RG'}))
    data_emissao = forms.DateField(required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Emissão'}))
    orgao_emissor = forms.CharField(required=False,
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Emissor'}))
    uf_emissao = forms.ChoiceField(choices=UF_options,
                                   required=False,
                                   widget=forms.Select(attrs={'class': 'form-select'}),
                                   initial='')
    filiacao = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control required',
                                                             'placeholder': 'Filiação'}))
    escolaridade = forms.ChoiceField(choices=escolaridade_options,
                                     widget=forms.Select(attrs={'class': 'form-select required'}),
                                     initial='')
    pcd = forms.BooleanField(required=False,
                             widget=forms.TextInput(attrs={'class': 'form-check-input required',
                                                           'role': 'switch'}))
    ps = forms.BooleanField(required=False,
                            widget=forms.TextInput(attrs={'class': 'form-check-input required',
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
    uf = forms.ChoiceField(choices=UF_options,
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
