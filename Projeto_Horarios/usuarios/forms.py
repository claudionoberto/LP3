from django import forms
from .models import Turma, Professor, Disciplina, Aula

class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ['nome_turma']

class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['nome_professor', 'email']

class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ['nome_disciplina', 'carga_horaria']

class AulaForm(forms.ModelForm):
    class Meta:
        model = Aula
        fields = ['turma', 'disciplina', 'professor', 'dia_semana', 'horario']