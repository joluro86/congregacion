from django.shortcuts import render
from admin_congregacion.models import *
from informes.models import EstadoInforme, InformeMensual, InformePublicador
from informes.views import limpiar_carro
from django.contrib import messages
import collections
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum, F
from django.core.paginator import Paginator


@login_required
def publicadores_congregacion(request):
    data = Publicador.objects.all()
    context={
        'publicadores': data.order_by('nombre'),
        'total': data.count()
    }

    return render(request, 'lista_publicadores_congregacion.html', context)


@login_required
def publicadores_congregacion_uno_a_uno(request):
    publicadores = Publicador.objects.all().order_by('nombre')
    

    # Create a paginator with a specified number of objects per page
    paginator = Paginator(publicadores, 1)

    # Get the page number from the request
    page_number = request.GET.get('page')

    publicador = publicadores[int(page_number)-1] if page_number else Publicador.objects.all().order_by('nombre').first()


    # Use the paginator to get the specified page
    page_obj = paginator.get_page(page_number)

    informes = InformePublicador.objects.filter(publicador=publicador)
    context = {
        'publicador': publicador,
        'informes': informes, 
        'page_obj': page_obj, 

        'total_pub': informes.aggregate(Sum('publicaciones'))['publicaciones__sum'],
        'total_vid': informes.aggregate(Sum('videos'))['videos__sum'],
        'total_horas': informes.aggregate(Sum('horas'))['horas__sum'],
        'total_revisitas': informes.aggregate(Sum('revisitas'))['revisitas__sum'],
        'total_cursos': informes.aggregate(Sum('cursos'))['cursos__sum'],
        'prom_pub': informes.aggregate(Avg('publicaciones'))['publicaciones__avg'],
        'prom_vid': informes.aggregate(Avg('videos'))['videos__avg'],
        'prom_horas': informes.aggregate(Avg('horas'))['horas__avg'],
        'prom_revisitas': informes.aggregate(Avg('revisitas'))['revisitas__avg'],
        'prom_cursos': informes.aggregate(Avg('cursos'))['cursos__avg'],

        'prom_pub_seis': informes[:6].aggregate(Avg('publicaciones'))['publicaciones__avg'],
        'prom_vid_seis': informes[:6].aggregate(Avg('videos'))['videos__avg'],
        'prom_hor_seis': informes[:6].aggregate(Avg('horas'))['horas__avg'],
        'prom_rev_seis': informes[:6].aggregate(Avg('revisitas'))['revisitas__avg'],
        'prom_cur_seis': informes[:6].aggregate(Avg('cursos'))['cursos__avg'],
    }

    return render(request, 'lista_publicadores_congregacion_uno_a_uno.html', context)


@login_required
def publicadores_por_grupo(request, id):
    try:
        grupos = Grupo.objects.all()
        grupo = Grupo.objects.get(numero=id)
        publicadores = Publicador.objects.filter(grupo=grupo)
        total_publicadores = publicadores.count()

        context = {
            'grupos': grupos,
            'publicadores_grupo': publicadores,
            'grupo': grupo,
            'total_publicadores': total_publicadores
        }

        if len(publicadores) < 1:
            messages.warning(request, 'Grupo sin publicadores registrados.')
        return render(request, 'grupos.html', context)
    except:
        messages.warning(request, 'Error en la busqueda.')
        grupos = Grupo.objects.all()
        return render(request, 'grupos.html', {'grupos': grupos})


@login_required
def ancianos(request):

    context = {
        'busqueda': 'Ancianos',
        'data': Publicador.objects.filter(tipo=3)
    }
    return render(request, 'ancianos_y_ministeriales.html', context)


@login_required
def ministeriales(request):

    context = {
        'busqueda': 'Siervos Ministeriales',
        'data': Publicador.objects.filter(tipo=4)
    }
    return render(request, 'ancianos_y_ministeriales.html', context)


@login_required
def grupos(request):
    grupos = Grupo.objects.all()
    limpiar_carro(request)
    return render(request, 'grupos.html', {'grupos': grupos})

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
        ultimos_seis_informes = InformeMensual.objects.filter(
            estado=EstadoInforme.objects.get(estado='Cerrado')).order_by('-id')[:6]
        publicadores = Publicador.objects.all()
        cont = 0
        posibles_inactivos = []

        for u in ultimos_seis_informes:
            informes_publicadores = InformePublicador.objects.filter(
                informe_mensual=u).filter(estado='0')
            for p in informes_publicadores:
                posibles_inactivos.append(p.publicador)

        for pub in posibles_inactivos:
            if collections.Counter(posibles_inactivos)[pub] == 6:
                if existencia_inactivo(pub) == False:
                    publi = PublicadorInactivo()
                    publi.publicador = pub
                    publi.save()

                    pub.estado = EstadoPublicador.objects.get(
                        estado='Inactivo')
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
    try:
        ultimos_seis_informes = InformeMensual.objects.filter(
            estado=EstadoInforme.objects.get(estado='Cerrado')).order_by('-id')[:6]
        posibles_irregulares = []

        for u in ultimos_seis_informes:
            informes_publicadores = InformePublicador.objects.filter(
                informe_mensual=u).filter(estado='0')
            for p in informes_publicadores:
                posibles_irregulares.append(p.publicador)

        for pub in posibles_irregulares:
            if collections.Counter(posibles_irregulares)[pub] < 6 and collections.Counter(posibles_irregulares)[pub] > 0:
                if existencia_irregular(pub) == False:
                    publi = PublicadorIrregular()
                    publi.publicador = pub
                    publi.save()

                    pub.estado = EstadoPublicador.objects.get(
                        estado='Irregular')
                    pub.save()

    except Exception as e:
        print("error " + str(e))


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
