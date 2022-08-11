from ast import For
from django.http import HttpResponse
from django.shortcuts import render

from admin_congregacion.models import *

# Create your views here.

def publicadores_por_grupo(request, id):
    grupo= Grupo.objects.get(numero=id)
    publicadores = Publicador.objects.filter(grupo=grupo)
    return render(request, 'publicadores_por_grupo.html', {'publicadores':publicadores} )

def grupos(request):
    grupos= Grupo.objects.all()
    return render(request, 'grupos.html', {'grupos':grupos})

