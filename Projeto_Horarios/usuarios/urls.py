from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),     # Rota para login
    path('home/', views.home_view, name='home'), 
    path('horarios/', views.horarios_view, name='horarios'),  # Rota para a página inicial
    path('cadastrar_aula/', views.cadastrar_aula, name='cadastrar_aula'),
    path('cadastrar-turma/', views.cadastrar_turma, name='cadastrar_turma'),
    path('cadastrar-professor/', views.cadastrar_professor, name='cadastrar_professor'),
    path('cadastrar-disciplina/', views.cadastrar_disciplina, name='cadastrar_disciplina'),
    path('excluir_aula/', views.excluir_aula, name='excluir_aula'),
    path('relatorios/', views.relatorios, name='relatorios'),
    path('relatorios/gerar', views.relatorios, name='relatorios_gerar'),
    path('relatorios/pdf/', views.relatorios_pdf, name='relatorios_pdf'),
]