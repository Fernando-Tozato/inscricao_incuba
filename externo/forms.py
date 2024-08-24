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
    nome = forms.CharField()
    nome_social = forms.CharField(required=False)
    nascimento = forms.DateField()
    cpf = forms.CharField(max_length=14)
    rg = forms.CharField(max_length=14, required=False)
    data_emissao = forms.DateField(required=False)
    orgao_emissor = forms.CharField(required=False)
    uf_emissao = forms.ChoiceField(choices=UF_options,
                                   required=False,
                                   widget=forms.Select(attrs={'class': 'form-select'}),
                                   initial='')
    filiacao = forms.CharField()
    escolaridade = forms.ChoiceField(choices=escolaridade_options,
                                     widget=forms.Select(attrs={'class': 'form-select required'}),
                                     initial='')
    pcd = forms.BooleanField()
    ps = forms.BooleanField()

    email = forms.EmailField(required=False)
    telefone = forms.CharField(required=False)
    celular = forms.CharField()

    cep = forms.CharField()
    rua = forms.CharField()
    numero = forms.CharField()
    complemento = forms.CharField(required=False)
    bairro = forms.CharField()
    cidade = forms.CharField()
    uf = forms.ChoiceField(choices=UF_options,
                           widget=forms.Select(attrs={'class': 'form-select required'}),
                           initial='')

    curso = forms.ChoiceField()
    dias = forms.ChoiceField()
    horario = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(InscricaoForm, self).__init__(*args, **kwargs)
        self.fields['uf_emissao'].widget.attrs.update({'class': 'form-select'})
        self.fields['escolaridade'].widget.attrs.update({'class': 'form-select required'})
        self.fields['uf'].widget.attrs.update({'class': 'form-select required'})
