from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User


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
