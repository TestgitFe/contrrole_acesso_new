from django.shortcuts import render, redirect
from .models import RegistroAcesso, Visitante, Endereco
from .forms import EnderecoForm, VeiculoForm, VisitanteForm, RegistroAcessorForm
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url="/contas/login/")
def index(request):
    acessos = RegistroAcesso.objects.all()
    context = { "acessos": acessos }
    return render(request, 'index.html', context)

def visitantes(requets):
    visitantes = Visitante.objects.all()
    context = { "visitantes": visitantes}
    return render(requets, 'visitante/index.html', context)

def novo_visitante(requets):
    form_endereco = EnderecoForm()
    form_visitante = VisitanteForm()
    form_veiculo = VeiculoForm()

    if requets.method == 'POST':
        form_endereco = EnderecoForm(requets.POST)
        form_visitante = VisitanteForm(requets.POST)
        form_veiculo = VeiculoForm(requets.POST)

        if form_visitante.is_valid() and form_endereco.is_valid() and form_veiculo.is_valid:
            visitante = form_visitante.save()
            endereco = form_endereco.save(commit=False)
            veiculo = form_veiculo.save(commit=False)
            veiculo.pessoa = visitante
            veiculo.save()
            endereco.pessoa = visitante
            endereco.save()
            return redirect('visitantes')

    context = { "form_endereco": form_endereco, "form_visitante": form_visitante, "form_veiculo": form_veiculo}
    return render(requets, 'visitante/new.html', context)

def visitante(request, visitante_id):
    visitante = get_object_or_404(Visitante, id=visitante_id)
    context = {"visitante" : visitante }
    return render(request, 'visitante/view.html' , context)

def editar_visitante(request, visitante_id):
    visitante = get_object_or_404(Visitante, id=visitante_id)
    form_visitante = VisitanteForm(instance=visitante)

    if request.method == 'POST':
        form_visitante = VisitanteForm(request.POST, instance=visitante)

        if form_visitante.is_valid():
            form_visitante.save()
            return redirect('visitante' , visitante.id)
    
    context = { "visitante": visitante, "form_visitante": form_visitante }

    return render(request, 'visitante/edit.html', context)

def registrar_acesso(request):
    form = RegistroAcessorForm()

    if request.method == 'POST':
        form = RegistroAcessorForm(request.POST)

        if form.is_valid():
            datetime.now()
            acesso = form.save(commit=False)
            acesso.data_hora_entrada = datetime.now()
            acesso.save()
            return redirect('index')
    
    context = { "form": form }

    return render(request, 'acesso/registrar.html', context)

def finalizar_acesso(request, acesso_id):
    acesso = get_object_or_404(RegistroAcesso, id=acesso_id)
    acesso.atualiza_status()
    return redirect(index)

    











    
    
    





            