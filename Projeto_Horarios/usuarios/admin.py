from django.contrib import admin
from .models import Turma, Professor, Disciplina, Aula

admin.site.register(Turma)
admin.site.register(Professor)
admin.site.register(Disciplina)
admin.site.register(Aula)