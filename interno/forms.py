from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User

from database.models import Turma, Curso, Unidade, Aluno, Controle


class MatriculaForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = [
            'nome', 'nome_social', 'nascimento', 'cpf', 'rg', 'data_emissao',
            'orgao_emissor', 'uf_emissao', 'filiacao', 'escolaridade', 'email',
            'telefone', 'celular', 'cep', 'rua', 'numero', 'complemento',
            'bairro', 'cidade', 'uf', 'pcd', 'ps', 'observacoes', 'id_turma'
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
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Observações'}),
            'id_turma': forms.Select(attrs={'class': 'd-none', 'id': 'id_turma'})
        }

    def __init__(self, *args, **kwargs):
        inscrito: [dict, None] = kwargs.pop('inscrito', None)
        super().__init__(*args, **kwargs)
        self.fields['nascimento'].input_formats = ['%d/%m/%Y', '%Y-%m-%d']
        self.fields['data_emissao'].input_formats = ['%d/%m/%Y', '%Y-%m-%d']

        if inscrito:
            self.fields['nome'].initial = inscrito['nome']
            self.fields['nome_social'].initial = inscrito['nome_social']
            self.fields['nascimento'].initial = inscrito['nascimento']
            self.fields['cpf'].initial = inscrito['cpf']
            self.fields['rg'].initial = inscrito['rg']
            self.fields['data_emissao'].initial = inscrito['data_emissao']
            self.fields['orgao_emissor'].initial = inscrito['orgao_emissor']
            self.fields['uf_emissao'].initial = inscrito['uf_emissao']
            self.fields['filiacao'].initial = inscrito['filiacao']
            self.fields['escolaridade'].initial = inscrito['escolaridade']
            self.fields['email'].initial = inscrito['email']
            self.fields['telefone'].initial = inscrito['telefone']
            self.fields['celular'].initial = inscrito['celular']
            self.fields['cep'].initial = inscrito['cep']
            self.fields['rua'].initial = inscrito['rua']
            self.fields['numero'].initial = inscrito['numero']
            self.fields['complemento'].initial = inscrito['complemento']
            self.fields['bairro'].initial = inscrito['bairro']
            self.fields['cidade'].initial = inscrito['cidade']
            self.fields['uf'].initial = inscrito['uf']
            self.fields['pcd'].initial = inscrito['pcd']
            self.fields['ps'].initial = inscrito['ps']
            self.fields['id_turma'].initial = inscrito['id_turma']

    def clean(self):
        cleaned_data = super().clean()
        cpf = cleaned_data.get("cpf")
        if Aluno.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError("Já existe um aluno cadastrado com este CPF.")
        return cleaned_data
    

class BuscaForm(forms.Form):
    busca = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': 'Busca'}))


class UnidadeForm(forms.ModelForm):
    class Meta:
        model = Unidade
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control required',
                                           'placeholder': 'Nome'}),
            'endereco1': forms.TextInput(attrs={'class': 'form-control required',
                                                'placeholder': 'Endereço principal'}),
            'endereco2': forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': 'Endereço secundário'})
        }


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = '__all__'
        widgets = {
            "nome": forms.TextInput(attrs={'class': 'form-control required',
                                           'placeholder': 'Nome'}),
            "descricao": forms.Textarea(attrs={'class': 'form-control required',
                                               'placeholder': 'Descricao'}),
            "requisitos": forms.Textarea(attrs={'class': 'form-control required',
                                                'placeholder': 'Requisitos'}),
            "imagem": forms.FileInput(attrs={'class': 'form-control required',
                                             'placeholder': 'Imagem'}),
            "unidades": forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input',}),
            "escolaridade": forms.Select(attrs={'class': 'form-select required',
                                                'placeholder': 'Escolaridade'}),
            "idade": forms.NumberInput(attrs={'class': 'form-control required',
                                              'placeholder': 'Idade'}),
        }



class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        exclude = ['num_alunos']
        widgets = {
            "curso": forms.Select(attrs={'class': 'form-control required',
                                           'placeholder': 'Curso'}),
            "dias": forms.TextInput(attrs={'class': 'form-control required',
                                               'placeholder': 'Dias da semana'}),
            "horario_entrada": forms.TimeInput(format='%H:%M',
                                               attrs={'class': 'form-control required',
                                                      'placeholder': 'Horário entrada',
                                                      'type': 'time'}),
            "horario_saida": forms.TimeInput(format='%H:%M',
                                             attrs={'class': 'form-control required',
                                                    'placeholder': 'Horário saída',
                                                    'type': 'time'}),
            "vagas": forms.NumberInput(attrs={'class': 'form-control required',
                                              'placeholder': 'Vagas'}),
            "professor": forms.TextInput(attrs={'class': 'form-control required',
                                                'placeholder': 'Professor'}),
            "unidade": forms.Select(choices=[('', 'Selecione...')],
                                    attrs={'class': 'form-select required',
                                           'disabled': 'true'}),
        }


class ControleForm(forms.ModelForm):
    class Meta:
        model = Controle
        fields = '__all__'
        widgets = {
            "inscricao_inicio": forms.DateTimeInput(format="%Y-%m-%dT%H:%M",
                                                    attrs={'class': 'form-control required',
                                                           'type': 'datetime-local'}),
            "inscricao_fim": forms.DateTimeInput(format="%Y-%m-%dT%H:%M",
                                                 attrs={'class': 'form-control required',
                                                        'type': 'datetime-local'}),
            "sorteio_data": forms.DateTimeInput(format="%Y-%m-%dT%H:%M",
                                                attrs={'class': 'form-control required',
                                                       'type': 'datetime-local'}),
            "matricula_sorte_inicio": forms.DateTimeInput(format="%Y-%m-%dT%H:%M",
                                                       attrs={'class': 'form-control required',
                                                              'type': 'datetime-local'}),
            "matricula_sorte_fim": forms.DateTimeInput(format="%Y-%m-%dT%H:%M",
                                                     attrs={'class': 'form-control required',
                                                            'type': 'datetime-local'}),
            "matricula_reman_inicio": forms.DateTimeInput(format="%Y-%m-%dT%H:%M",
                                                   attrs={'class': 'form-control required',
                                                          'type': 'datetime-local'}),
            "matricula_reman_fim": forms.DateTimeInput(format="%Y-%m-%dT%H:%M",
                                                 attrs={'class': 'form-control required',
                                                        'type': 'datetime-local'}),
            "aulas_inicio": forms.DateTimeInput(format="%Y-%m-%dT%H:%M",
                                                attrs={'class': 'form-control required',
                                                       'type': 'datetime-local'}),
            "aulas_fim": forms.DateTimeInput(format="%Y-%m-%dT%H:%M",
                                             attrs={'class': 'form-control required',
                                                    'type': 'datetime-local'}),
        }

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
    new_password1 = forms.CharField(label='Senha',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control required',
                                                                      'placeholder': 'Senha'}))
    new_password2 = forms.CharField(label='Confirme sua senha',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control required',
                                                                      'placeholder': 'Confirme de senha'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].label = "Senha"
        self.fields['new_password2'].label = "Confirmação da Senha"

class EmailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))