from rest_framework import serializers
from .models import Inscrito, Turma, Sorteado, Aluno

class InscritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscrito
        fields = '__all__'

class TurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = '__all__'

class SorteadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sorteado
        fields = '__all__'

class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = '__all__'