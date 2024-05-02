from rest_framework import serializers
from .models import Sorteado, Aluno

class SorteadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sorteado
        fields = '__all__'

class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = '__all__'