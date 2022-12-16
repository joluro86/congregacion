from django.shortcuts import render
from admin_congregacion.models import *
from informes.models import EstadoInforme, InformeMensual, InformePublicador
from informes.views import limpiar_carro
from django.contrib import messages
import collections
from django.contrib.auth.decorators import login_required
from django.db.models import F

@login_required
def publicadores_congregacion(request):
    context={
        'publicadores': Publicador.objects.all().order_by('nombre')
    }

    return render(request, 'lista_publicadores_congregacion.html', context)

@login_required
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

@login_required
def ancianos(request):

    context={
        'busqueda': 'Ancianos', 
        'data': Publicador.objects.filter(tipo=3)
    }
    return render(request, 'ancianos_y_ministeriales.html', context)

@login_required
def ministeriales(request):

    context={
        'busqueda': 'Siervos Ministeriales', 
        'data': Publicador.objects.filter(tipo=4)
    }
    return render(request, 'ancianos_y_ministeriales.html', context)

@login_required
def grupos(request):
    grupos= Grupo.objects.all()
    limpiar_carro(request)
    return render(request, 'grupos.html', {'grupos':grupos})

# INICIO PUBLICADORES INACTIVOS
@login_required
def calculo_inactivos(request):
    PublicadorInactivo.objects.all().delete()
    calculo_publicador_inactivo()

    context = {
        'publicadores_inactivos': PublicadorInactivo.objects.all().order_by(F('publicador__grupo').asc())
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

                    pub.estado = EstadoPublicador.objects.get(estado='Inactivo')
                    pub.save()
                          
    except:
        print("error")

def existencia_inactivo(publicador):
    if PublicadorInactivo.objects.filter(publicador=publicador):
        return True
    else:
        return False

@login_required
def publicadores_inactivos(request):
    context = {
        'publicadores_inactivos': PublicadorInactivo.objects.all().order_by(F('publicador__grupo').asc())
    }
    return render(request, 'inactivos.html', context)

# FIN PUBLICADORES INACTIVOS

# INICIO PUBLICADORES IRREGULARES
@login_required
def calculo_irregulares(request):
    
    PublicadorIrregular.objects.all().delete()
    calculo_publicador_irregular()

    context = {
        'publicadores_irregulares': PublicadorIrregular.objects.all().order_by(F('publicador__grupo').asc())
    }

    return render(request, 'irregulares.html', context)

def calculo_publicador_irregular():
    print("irregular aqui")
    try:
        ultimos_seis_informes = InformeMensual.objects.filter(estado=EstadoInforme.objects.get(estado='Cerrado')).order_by('-id')[:6]
        posibles_irregulares=[]

        for u in ultimos_seis_informes:
            informes_publicadores = InformePublicador.objects.filter(informe_mensual=u).filter(estado='0')
            print(u)
            for p in informes_publicadores:
                posibles_irregulares.append(p.publicador)
        
        for pub in posibles_irregulares:
            print(pub)
            if collections.Counter(posibles_irregulares)[pub]<6 and collections.Counter(posibles_irregulares)[pub]>0:
                if existencia_irregular(pub)==False:
                    publi = PublicadorIrregular()
                    publi.publicador=pub
                    publi.save()  

                    pub.estado = EstadoPublicador.objects.get(estado='Irregular')
                    pub.save()
                          
    except Exception as e:
        print("error " + str(e) )

def existencia_irregular(publicador):
    if PublicadorIrregular.objects.filter(publicador=publicador):
        return True
    else:
        return False

@login_required
def publicadores_irregulares(request):
    context = {
        'publicadores_irregulares': PublicadorIrregular.objects.all().order_by(F('publicador__grupo').asc())
    }
    return render(request, 'irregulares.html', context)

# FIN PUBLICADORES IRREGULARES