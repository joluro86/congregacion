from urllib import request
from django.shortcuts import render
from admin_congregacion.forms import PublicadorForm
from admin_congregacion.models import *
from informes.views import limpiar_carro
from django.views.generic import ListView, CreateView
from django.contrib import messages

class Crear_Publicador(CreateView):
    #login_url = 'login'
    template_name = 'create_publicador.html'
    form_class = PublicadorForm
    success_url = '/clientes/lista_clientes/'

def publicadores_por_grupo(request, id):
    try:
        grupos= Grupo.objects.all()
        grupo= Grupo.objects.get(numero=id)
        publicadores = Publicador.objects.filter(grupo=grupo)
        
        if len(publicadores)<1:
            messages.warning(request, 'Grupo sin publicadores registrados.')
        return render(request, 'grupos.html', {'grupos':grupos, 'publicadores_grupo':publicadores, 'grupo':grupo} )
    except:
        messages.warning(request, 'Error en la busqueda.')
        grupos= Grupo.objects.all()
        return render(request, 'grupos.html', {'grupos':grupos} )

def grupos(request):
    grupos= Grupo.objects.all()
    limpiar_carro(request)
    return render(request, 'grupos.html', {'grupos':grupos})

