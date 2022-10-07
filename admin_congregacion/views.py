from django.shortcuts import render
from admin_congregacion.forms import PublicadorForm
from admin_congregacion.models import *
from informes.models import InformePublicador
from informes.views import limpiar_carro
from django.views.generic import CreateView
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

def publicadores_inactivos(request):
    publicadores = Publicador.objects.all()

    PublicadorInactivo.objects.all().delete()
    
    for p in publicadores:
        calculo_publicador_inactivo(request, p)

    publicadores_inactivos = PublicadorInactivo.objects.all()
    context = {
        'publicadores_inactivos': publicadores_inactivos
    }
    return render(request, 'inactivos.html', context)

def calculo_publicador_inactivo(request, publicador):
    try:
        informes_publicador = InformePublicador.objects.filter(publicador=publicador).order_by('-id')[0:6]
        cont=0
        for i in informes_publicador:
            if str(i.horas)=='0':
                cont+=1  
                print(cont)          
            if cont==6:
                inactivo = PublicadorInactivo()
                inactivo.publicador = i.publicador
                inactivo.save()     
    except:
        print("error")