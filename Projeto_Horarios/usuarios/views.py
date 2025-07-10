from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import TurmaForm, ProfessorForm, DisciplinaForm
from .models import Turma, Professor, Disciplina, Aula
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.http import HttpResponse
import weasyprint

def login_view(request):
    if request.method == 'GET':
        return render(request, 'usuarios/login.html')
    
    elif request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/home')  # Redireciona para a home
        else:
            return render(request, 'usuarios/login.html', {
                'erro': 'Usuário ou senha inválidos'
            })
    
    else:
        return HttpResponseBadRequest()

def home_view(request):
    turmas = Turma.objects.all()
    disciplinas = Disciplina.objects.all()
    professores = Professor.objects.all()
    aulas = Aula.objects.all()
    return render(request, 'usuarios/home.html', {
        'turmas': turmas,
        'disciplinas': disciplinas,
        'professores': professores,
        'aulas': aulas,
    })

def horarios_view(request):
    turmas = Turma.objects.all()
    disciplinas = Disciplina.objects.all()
    professores = Professor.objects.all()
    turma_id = request.GET.get('turma_id')
    turma_selecionada = None
    if turma_id:
        aulas = Aula.objects.filter(turma_id=turma_id)
        turma_selecionada = Turma.objects.get(id=turma_id)
    else:
        aulas = Aula.objects.none()  # Não mostra nenhuma aula
    dias_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']
    horarios_periodos = [
        ('1ª aula', '7:00 - 7:50'),
        ('2ª aula', '7:50 - 8:40'),
        ('3ª aula', '8:40 - 9:30'),
        ('4ª aula', '9:50 - 10:40'),
        ('5ª aula', '10:40 - 11:30'),
        ('6ª aula', '11:30 - 12:20'),
    ]
    return render(request, 'usuarios/horarios.html', {
        'turmas': turmas,
        'disciplinas': disciplinas,
        'professores': professores,
        'aulas': aulas,
        'turma_selecionada': turma_selecionada,
        'dias_semana': dias_semana,
        'horarios_periodos': horarios_periodos,
    })

def cadastrar_turma(request):
    if request.method == 'POST':
        form = TurmaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return redirect('home')

def cadastrar_professor(request):
    if request.method == 'POST':
        form = ProfessorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return redirect('home')

def cadastrar_disciplina(request):
    if request.method == 'POST':
        form = DisciplinaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return redirect('home')

def cadastrar_aula(request):
    if request.method == 'POST':
        turma_id = request.POST.get('turma_id')
        disciplina_id = request.POST.get('disciplina_id')
        professor_id = request.POST.get('professor_id')
        dia_semana = request.POST.get('dia_semana')
        horario = request.POST.get('horario')

        try:
            turma = Turma.objects.get(id=turma_id)
            disciplina = Disciplina.objects.get(id=disciplina_id)
            professor = Professor.objects.get(id=professor_id)
        except (Turma.DoesNotExist, Disciplina.DoesNotExist, Professor.DoesNotExist):
            return HttpResponseBadRequest("Dados inválidos")

        Aula.objects.create(
            turma=turma,
            disciplina=disciplina,
            professor=professor,
            dia_semana=dia_semana,
            horario=horario
        )
        return redirect('home')
    
    return HttpResponseBadRequest()

@require_POST
def excluir_aula(request):
    aula_id = request.POST.get('aula_id')
    if aula_id:
        try:
            aula = Aula.objects.get(id=aula_id)
            aula.delete()
        except Aula.DoesNotExist:
            pass
    return redirect('home')

def relatorios(request):
    turmas = Turma.objects.all()
    professores = Professor.objects.all()
    disciplinas = Disciplina.objects.all()
    resultados = Aula.objects.all()

    turma_id = request.GET.get('turma_id')
    professor_id = request.GET.get('professor_id')
    disciplina_id = request.GET.get('disciplina_id')

    if turma_id:
        resultados = resultados.filter(turma_id=turma_id)
    if professor_id:
        resultados = resultados.filter(professor_id=professor_id)
    if disciplina_id:
        resultados = resultados.filter(disciplina_id=disciplina_id)

    return render(request, 'usuarios/relatorio.html', {
        'turmas': turmas,
        'professores': professores,
        'disciplinas': disciplinas,
        'resultados': resultados
    })

def relatorios_pdf(request):
    turmas = Turma.objects.all()
    professores = Professor.objects.all()
    disciplinas = Disciplina.objects.all()
    resultados = Aula.objects.all()

    turma_id = request.GET.get('turma_id')
    professor_id = request.GET.get('professor_id')
    disciplina_id = request.GET.get('disciplina_id')

    if turma_id:
        resultados = resultados.filter(turma_id=turma_id)
    if professor_id:
        resultados = resultados.filter(professor_id=professor_id)
    if disciplina_id:
        resultados = resultados.filter(disciplina_id=disciplina_id)

    html_string = render_to_string('usuarios/relatorio_pdf.html', {
        'resultados': resultados,
        'turmas': turmas,
        'professores': professores,
        'disciplinas': disciplinas,
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="relatorio.pdf"'
    weasyprint.HTML(string=html_string).write_pdf(response)
    return response