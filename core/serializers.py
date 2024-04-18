from rest_framework import serializers
from .models import Turmas, Contatos, Enderecos, Alunos

class TurmasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turmas
        fields = '__all__'

class ContatosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contatos
        fields = '__all__'

class EnderecosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enderecos
        fields = '__all__'

class AlunosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alunos
        fields = '__all__'