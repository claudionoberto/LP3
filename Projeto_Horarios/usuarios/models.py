from django.db import models

class Turma(models.Model):
    nome_turma = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_turma

class Professor(models.Model):
    nome_professor = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nome_professor

class Disciplina(models.Model):
    nome_disciplina = models.CharField(max_length=100)
    carga_horaria = models.PositiveIntegerField()

    def __str__(self):
        return self.nome_disciplina

class Aula(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    dia_semana = models.CharField(max_length=20)
    horario = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.turma} - {self.disciplina} - {self.professor} ({self.dia_semana}, {self.horario})"
