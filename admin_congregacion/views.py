from django.shortcuts import render
from admin_congregacion.forms import PublicadorForm
from admin_congregacion.models import *
from informes.models import EstadoInforme, InformeMensual, InformePublicador
from informes.views import limpiar_carro
from django.views.generic import CreateView
from django.contrib import messages
import collections

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

def calculo_inactivos(request):

    PublicadorInactivo.objects.all().delete()
    calculo_publicador_inactivo()

    context = {
        'publicadores_inactivos': PublicadorInactivo.objects.all()
    }

    return render(request, 'inactivos.html', context)

def calculo_publicador_inactivo():
    try:
        ultimos_seis_informes = InformeMensual.objects.filter(estado=EstadoInforme.objects.get(estado='Cerrado')).order_by('-id')[:6]
        publicadores = Publicador.objects.all()        
        cont=0
        posibles_inactivos=[]

        for u in ultimos_seis_informes:
            informes_publicadores = InformePublicador.objects.filter(informe_mensual=u).filter(estado='0')
            for p in informes_publicadores:
                posibles_inactivos.append(p.publicador)
        
        for pub in posibles_inactivos:
            if collections.Counter(posibles_inactivos)[pub]==6:
                if existencia_inactivo(pub)==False:
                    publi = PublicadorInactivo()
                    publi.publicador=pub
                    publi.save()        
    except:
        print("error")

def existencia_inactivo(publicador):
    if PublicadorInactivo.objects.filter(publicador=publicador):
        return True
    else:
        return False

def publicadores_inactivos(request):
    context = {
        'publicadores_inactivos': PublicadorInactivo.objects.all()
    }

    return render(request, 'inactivos.html', context)