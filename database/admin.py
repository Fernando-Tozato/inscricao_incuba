from django.contrib import admin
from .models import Inscrito, Turma, Sorteado, Aluno

admin.site.register(Inscrito)
admin.site.register(Turma)
admin.site.register(Sorteado)
admin.site.register(Aluno)