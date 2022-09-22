from urllib import request
from django.shortcuts import render, redirect
from admin_congregacion.models import *
from informes.models import InformePublicador
from informes.views import limpiar_carro
from django.views.generic import ListView
from django.contrib import messages

def publicadores_por_grupo(request, id):
    grupos= Grupo.objects.all()
    grupo= Grupo.objects.get(numero=id)
    publicadores = Publicador.objects.filter(grupo=grupo)
    if len(publicadores)<1:
        messages.warning(request, 'Grupo sin publicadores registrados.')
    return render(request, 'grupos.html', {'grupos':grupos, 'publicadores_grupo':publicadores, 'grupo':grupo} )

def grupos(request):
    grupos= Grupo.objects.all()
    limpiar_carro(request)
    return render(request, 'grupos.html', {'grupos':grupos})

