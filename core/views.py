from django.contrib.auth import login
from django.http import response
from django.shortcuts import redirect, render
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

#def index(request):
#    return redirect('agenda/')

def login_user(request):
    return render(request, 'login.html') 

def logout_user(request):
    logout(request)
    return redirect('/')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, "Usuário ou senha inválido")
            
    return redirect('/')

@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        local = request.POST.get('local')
        usuario = request.user
        id_evento = request.POST.get('id_evento')
        if id_evento:
            evento = Evento.objects.get(id=id_evento)
            if usuario ==usuario:
                evento.titulo = titulo
                evento.descricao = descricao
                evento.data_evento = data_evento
                evento.local = local
                evento.save()
        #if id_evento:
        #    Evento.objects.filter(id=id_evento).update(titulo=titulo,
        #    data_evento=data_evento, descricao=descricao, local=local)
        else:
            Evento.objects.create(titulo=titulo,
            data_evento=data_evento, descricao=descricao,
            usuarios= usuario, local=local)

    return redirect('/')

@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'evento.html', dados)


@login_required(login_url='/login/')
def lista_eventos(request):

    usuarios = request.user
    evento = Evento.objects.filter(usuarios=usuarios)
    dados = {'eventos': evento}
    return render(request, 'agenda.html', dados)


login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user
    evento = Evento.objects.get(id=id_evento)
    if usuario == evento.usuarios:
        evento.delete()
    return redirect('/')