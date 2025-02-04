from datetime import datetime

from django import forms
from django.utils import timezone

from database.models import Inscrito, Turma


class InscricaoForm(forms.ModelForm):
    class Meta:
        model = Inscrito
        fields = [
            'nome', 'nome_social', 'nascimento', 'cpf', 'rg', 'data_emissao',
            'orgao_emissor', 'uf_emissao', 'filiacao', 'escolaridade', 'email',
            'telefone', 'celular', 'cep', 'rua', 'numero', 'complemento',
            'bairro', 'cidade', 'uf', 'pcd', 'ps', 'id_turma'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control required', 'placeholder': 'Nome'}),
            'nome_social': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome social'}),
            'nascimento': forms.DateInput(attrs={'class': 'form-control required', 'placeholder': 'Nascimento', 'type': 'date'}, format='%Y-%m-%d'),
            'cpf': forms.TextInput(attrs={'class': 'form-control required', 'placeholder': 'CPF'}),
            'rg': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RG'}),
            'data_emissao': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Emissão', 'type': 'date'}, format='%Y-%m-%d'),
            'orgao_emissor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Emissor'}),
            'uf_emissao': forms.Select(attrs={'class': 'form-select'}),
            'filiacao': forms.TextInput(attrs={'class': 'form-control required', 'placeholder': 'Filiação'}),
            'escolaridade': forms.Select(attrs={'class': 'form-select required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone'}),
            'celular': forms.TextInput(attrs={'class': 'form-control required', 'placeholder': 'Celular'}),
            'cep': forms.TextInput(attrs={'class': 'form-control required', 'placeholder': 'CEP'}),
            'rua': forms.TextInput(attrs={'class': 'form-control required', 'placeholder': 'Rua'}),
            'numero': forms.TextInput(attrs={'class': 'form-control required', 'placeholder': 'Número'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Complemento'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control required', 'placeholder': 'Bairro'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control required', 'placeholder': 'Cidade'}),
            'uf': forms.Select(attrs={'class': 'form-select required'}),
            'pcd': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
            'ps': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
            'id_turma': forms.Select(attrs={'class': 'd-none', 'id': 'id_turma'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        today = datetime.strftime(timezone.now().date(), '%Y-%m-%d')

        self.fields['nascimento'].input_formats = ['%d/%m/%Y', '%Y-%m-%d']
        self.fields['nascimento'].widget.attrs.update({
            'min': '1900-01-01',
            'max': today
        })

        self.fields['data_emissao'].input_formats = ['%d/%m/%Y', '%Y-%m-%d']
        self.fields['data_emissao'].widget.attrs.update({
            'min': '1900-01-01',
            'max': today
        })

    def clean(self):
        cleaned_data = super().clean()

        cpf = cleaned_data.get("cpf")
        if Inscrito.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError("Já existe um inscrito com este CPF.")

        data_nasc = cleaned_data.get("nascimento")
        data_emissao = cleaned_data.get("data_emissao")

        if data_nasc and data_emissao:
            if data_nasc < data_emissao:
                raise Exception('Data de nascimento não pode ser menor que a data de emissão do RG.')


class ResultadoForm(forms.Form):
    id_turma = forms.ModelChoiceField(queryset=Turma.objects.all(),
                                      widget=forms.Select(attrs={'class': 'd-none', 'id': 'id_turma'}))

    def __init__(self, *args, **kwargs):
        turma = kwargs.pop('turma', None)
        super().__init__(*args, **kwargs)

        if turma:
            self.fields['id_turma'].initial = turma
