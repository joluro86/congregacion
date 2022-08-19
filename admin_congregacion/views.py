from django.shortcuts import render
from admin_congregacion.models import *

def publicadores_por_grupo(request, id):
    grupos= Grupo.objects.all()
    grupo= Grupo.objects.get(numero=id)
    publicadores = Publicador.objects.filter(grupo=grupo)
    total = publicadores.count()

    return render(request, 'grupos.html', {'grupos':grupos, 'publicadores_grupo':publicadores, 'grupo':grupo} )

def grupos(request):
    grupos= Grupo.objects.all()
    return render(request, 'grupos.html', {'grupos':grupos})



