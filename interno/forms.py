from django import forms

class Busca_CPF(forms.Form):
    cpf = forms.CharField(max_length=14)