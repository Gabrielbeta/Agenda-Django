from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import response
from django.shortcuts import redirect, render
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse

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
        usuario = authenticate(username=request.POST.get('username'), password=password)
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
        if id_evento: #se não houver id evento ele não executa
            evento = Evento.objects.get(id=id_evento)
            if usuario == usuario:
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
    data_atual = datetime.now() - timedelta(hours=1)
    evento = Evento.objects.filter(usuarios=usuarios, data_evento__gt=data_atual)
    dados = {'eventos': evento}
    return render(request, 'agenda.html', dados)




login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user
    try:
       evento = Evento.objects.get(id=id_evento) 
    except Exception:
        raise Http404()
    if usuario == evento.usuarios:
        evento.delete()
    else:
        raise Http404()
    return redirect('/')


def json_lista_evento(request, id_usuario):
    usuarios = User.objects.get(id=id_usuario)
    evento = Evento.objects.filter(usuarios=usuarios).values('id', 'titulo')
    return JsonResponse(list(evento), safe=False)

@login_required(login_url='/login/')
def eventos_passados(request):
    pessoa_que_esta_usando = request.user
    data_agora = datetime.now() - timedelta(hours=1)
    eventos_atrados = Evento.objects.filter(usuarios=pessoa_que_esta_usando, data_evento__lt=data_agora)
    lista_eventos_atrasados = {'eventos_atrasados':eventos_atrados}
    return render (request, 'events_pass.html', lista_eventos_atrasados)
