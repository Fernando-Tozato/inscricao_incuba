from pyexpat import model
from rest_framework import serializers
from .models import *

class InscritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscrito
        fields = '__all__'

class TurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = '__all__'

class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = '__all__'

class ControleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Controle
        fields = '__all__'