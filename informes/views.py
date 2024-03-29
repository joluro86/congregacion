from django.shortcuts import render, redirect
from django.contrib import messages
from admin_congregacion.models import Grupo, PivoteUserToSuperintendente, Publicador
from informes.carro_informe_grupo import Carro_informe
from informes.forms import InfomeMensualForm
from informes.models import UltimoInforme, InformeMensual, InformePublicador, PivoteInformeMensualGrupo
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Sum


@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def Crear_Informe_Actual(request):

    if (request.method == 'POST'):
        mes = request.POST.get('mes')
        año = request.POST.get('año')

        if validar_existencia_informe(mes, año):
            formset = InfomeMensualForm(request.POST)
            messages.warning(request, 'Informe ya existe.')
            return render(request, 'informe_Actual.html', {'form': formset})

        informes_abiertos = InformeMensual.objects.filter(estado='1')
        if len(informes_abiertos) == 0:
            formset = InfomeMensualForm(request.POST)
            if formset.is_valid():
                formset.save()
                calculo_ultimo_informe()

        else:
            formset = InfomeMensualForm(request.POST)
            messages.warning(
                request, 'No se pudo crear este registro debido a que existen informes pendientes por cerrar.')
            return render(request, 'informe_Actual.html', {'form': formset})

    formset = InfomeMensualForm()
    return render(request, 'informe_Actual.html', {'form': formset})


def calculo_ultimo_informe():
    try:
        informes_abiertos = InformeMensual.objects.filter(estado='1')
        if len(informes_abiertos) == 1:
            for i in informes_abiertos:
                UltimoInforme.objects.all().delete()
                ultimoinforme = UltimoInforme()
                ultimoinforme.informe = i
                ultimoinforme.save()
    except:
        pass


def validar_existencia_informe(mes, año):
    validar_informe = InformeMensual.objects.filter(mes=mes).filter(año=año)
    if len(validar_informe) > 0:
        return True


def validar_pivote_informe_grupo(grupo, mes):
    informes = PivoteInformeMensualGrupo.objects.filter(
        grupo=grupo).filter(informe_mensual=mes)
    if len(informes) > 0:
        return True


@login_required
def nuevo_informe(request, id):
    try:
        if request.user.is_authenticated:
            user = request.user
            pivote = PivoteUserToSuperintendente.objects.get(user=user)

            if (str(id) == str(pivote.grupo.numero)) or user.is_staff:

                informes_abiertos = InformeMensual.objects.filter(estado='1')
                grupo = Grupo.objects.get(numero=id)

                if len(Publicador.objects.filter(grupo=grupo)) < 1:
                    messages.warning(
                        request, 'Registre publicadores en este grupo para enviar informes.')
                    return redirect('publicadores_por_grupo', id)

                for i in informes_abiertos:
                    inf_mes = i

                try:
                    if validar_pivote_informe_grupo(grupo, inf_mes):
                        messages.warning(
                            request, 'El informe de este grupo ya fue ingresado.')
                        return redirect('publicadores_por_grupo', id)
                except Exception as e:
                    print(e)

                if len(informes_abiertos) == 0:
                    messages.warning(
                        request, 'No existen informes pendientes. Comuniquese con el administrador.')
                    return redirect('grupos')
                elif len(informes_abiertos) > 1:
                    messages.warning(
                        request, 'Existe mas de un informe pendiente. Habilite solo uno.')
                    return redirect('grupos')
                else:
                    publicadores = Publicador.objects.filter(grupo=grupo)
                    if len(publicadores) < 1:
                        messages.warning(
                            request, 'Debe registrar publicadores en este grupo.')
                        return redirect('grupos')
                    try:
                        grupo_informe = request.session.get('grupo')
                    except:
                        grupo_informe = request.session.get('grupo', '0')
                    finally:
                        if str(grupo_informe) != str(id):
                            limpiar_carro(request)

                    carro = Carro_informe(request)
                    for p in publicadores:
                        carro.agregar(p)
            else:
                messages.warning(
                    request, 'No tiene permisos para registrar este informe.')
                return redirect('grupos')

            for i in informes_abiertos:
                inf_mes = i

            return render(request, 'nuevo_informe.html', {'grupo': grupo, 'informe_mensual': inf_mes})
        else:
            messages.warning(request, 'No tiene permiso para esta función.')
            return redirect('grupos')
    except Exception as e:
        messages.warning(request, 'Error en la busqueda.' + repr(e))
        return redirect('grupos')


@login_required
def guardar_informe_grupo(request, id):
    if request.method == "POST":
        id_publicador = request.POST.get("id")
        p = request.POST.get("pub")
        v = request.POST.get("vid")
        h = request.POST.get("hor")

        try:
            if len(h) < 1:
                h = 0
            if int(h) <= 0:
                h = 0
        except:
            pass

        r = request.POST.get("rev")
        c = request.POST.get("cur")
        o = request.POST.get("obs")

        carro_informe = Carro_informe(request)
        carro_informe.cambiar_cantidad_informe(id_publicador, p, v, h, r, c, o)
        request.session['grupo'] = request.POST.get("grupo")
    return redirect('nuevo_informe', id=id)


@login_required
def finalizar_informe(request, id):

    validar_errores_informe_a_guardar(request, id)
    print(request.session['error_informes'])
    
    if request.session['error_informes'] == True:
        return redirect('nuevo_informe', id)        
    else:
        try:
            mes_informe = InformeMensual.objects.all()
            mes = ''
            for m in mes_informe:
                if str(m.estado) == 'Abierto':
                    mes = m
            for key, value in request.session.get("carro").items():
                print(value)
                inf = InformePublicador()
                inf.informe_mensual = mes
                inf.publicador = Publicador.objects.get(id=value['id'])
                inf.publicaciones = value['publicaciones']
                inf.videos = value['videos']
                inf.horas = value['horas']
                inf.revisitas = value['revisitas']
                inf.cursos = value['cursos']
                inf.observaciones = value['observaciones']
                inf.estado = value['estado']
                inf.save()

            pivote_informe_grupo = PivoteInformeMensualGrupo()
            pivote_informe_grupo.grupo = Grupo.objects.get(numero=id)
            pivote_informe_grupo.informe_mensual = mes
            pivote_informe_grupo.save()

            limpiar_carro(request)

            messages.warning(request, 'Informe guardado con existo.')
            print("try")

        except Exception as e:
            messages.warning(request, 'El informe no pudo ser creado.')
            print(e)
        print("else")
        return redirect('publicadores_por_grupo', id)      

def validar_errores_informe_a_guardar(request, id_grupo):

    request.session['error_informes'] = {}
    request.session.modified = True

    mes_informe = InformeMensual.objects.all()
    mes = ''
    for m in mes_informe:

        if str(m.estado) == 'Abierto':
            mes = m

    for key, value in request.session.get("carro").items():

        if (str(value['horas']) == "0" or str(value['horas']) == "") and str(value['observaciones']) == "":
            messages.warning(
                request, 'El informe no pudo ser creado. Si un publicador no informa horas debe ingresar la observación o marcarlo como activo.')
            request.session['error_informes'] = True
            break

        inf = InformePublicador()
        inf.informe_mensual = mes
        inf.publicador = Publicador.objects.get(id=value['id'])

        if int(value['cursos']) > 0 and int(value['revisitas']) < 1:
            messages.warning(request, 'El informe no pudo ser creado. ' +
                             str(inf.publicador)+' informó cursos biblicos sin revisitas.')
            request.session['error_informes'] = True
            break

        if int(value['horas']) > 200:
            messages.warning(request, 'El informe no pudo ser creado. ' +
                             str(inf.publicador)+' informó mas de 200 horas.')
            request.session['error_informes'] = True
            break

        if int(value['cursos']) > int(value['revisitas']):
            messages.warning(request, 'El informe no pudo ser creado. ' + str(
                inf.publicador)+' informó mas cursos biblicos que revisitas.')
            request.session['error_informes'] = True
            break

        request.session['error_informes'] = False


def limpiar_carro(request):
    request.session['carro'] = {}
    request.session.modified = True


def cancelar_informe(request):
    limpiar_carro(request)
    return redirect('grupos')


class InformeMensualList(LoginRequiredMixin, ListView):
    model = InformeMensual
    template_name = "list_informes_mensuales.html"


@login_required
def lista_informes_publicador(request, id):
    try:
        publicador = Publicador.objects.get(id=id)
        informes = InformePublicador.objects.filter(publicador=publicador)

        if len(informes) < 1:
            messages.warning(
                request, 'Publicador no tiene informes registrados.')
            return redirect('publicadores_por_grupo', publicador.grupo.numero)
        else:
            informes_seis_meses = InformePublicador.objects.filter(publicador=publicador).order_by('-id')
            data = {
                'informes': informes, 
                'publicador': publicador,
                'total_pub': InformePublicador.objects.filter(publicador=publicador).aggregate(Sum('publicaciones'))['publicaciones__sum'],
                'total_vid': InformePublicador.objects.filter(publicador=publicador).aggregate(Sum('videos'))['videos__sum'],
                'total_horas': InformePublicador.objects.filter(publicador=publicador).aggregate(Sum('horas'))['horas__sum'],
                'total_revisitas': InformePublicador.objects.filter(publicador=publicador).aggregate(Sum('revisitas'))['revisitas__sum'],
                'total_cursos': InformePublicador.objects.filter(publicador=publicador).aggregate(Sum('cursos'))['cursos__sum'],
                'prom_pub': InformePublicador.objects.filter(publicador=publicador).aggregate(Avg('publicaciones'))['publicaciones__avg'],
                'prom_vid': InformePublicador.objects.filter(publicador=publicador).aggregate(Avg('videos'))['videos__avg'],
                'prom_horas': InformePublicador.objects.filter(publicador=publicador).aggregate(Avg('horas'))['horas__avg'],
                'prom_revisitas': InformePublicador.objects.filter(publicador=publicador).aggregate(Avg('revisitas'))['revisitas__avg'],
                'prom_cursos': InformePublicador.objects.filter(publicador=publicador).aggregate(Avg('cursos'))['cursos__avg'],

                'prom_pub_seis': informes_seis_meses[:6].aggregate(Avg('publicaciones'))['publicaciones__avg'],
                'prom_vid_seis': informes_seis_meses[:6].aggregate(Avg('videos'))['videos__avg'],
                'prom_hor_seis': informes_seis_meses[:6].aggregate(Avg('horas'))['horas__avg'],
                'prom_rev_seis': informes_seis_meses[:6].aggregate(Avg('revisitas'))['revisitas__avg'],
                'prom_cur_seis': informes_seis_meses[:6].aggregate(Avg('cursos'))['cursos__avg'],
                }
            return render(request, 'lista_informes_publicador.html', data)

    except Exception as e:
        messages.warning(request, 'Publicador no tiene informes registrados.')
        print(e)
        return redirect('grupos')


@login_required
def busqueda_informe_mensual(request, id):

    try:
        informe_mensual = InformeMensual.objects.get(id=id)
        request.session['informe_mensual'] = {}
        request.session.modified = True
        request.session['informe_mensual'] = informe_mensual.id

        informes = InformePublicador.objects.filter(
            informe_mensual=informe_mensual)
    except:
        informes = {}
        messages.warning(request, 'Error al buscar informes.')
        grupos = Grupo.objects.all()

        context = {
            'informes': informes,
            'grupos': grupos,
            'informe_mensual': None
        }

        return render(request, 'historico.html', context)

    grupos = Grupo.objects.all()

    context = {
        'informes': informes,
        'grupos': grupos,
        'informe_mensual': informe_mensual
    }

    return render(request, 'historico.html', context)


@login_required
def busqueda_informe_mensual_id_grupo(request, id):

    try:
        informe_mensual = InformeMensual.objects.get(
            id=request.session['informe_mensual'])
        grupo = Grupo.objects.get(numero=id)

        publicadores = Publicador.objects.filter(grupo=grupo)
        informes = []
        for p in publicadores:
            infor = InformePublicador.objects.filter(
                publicador=p).filter(informe_mensual=informe_mensual)
            for i in infor:
                informes.append(i)
    except:
        informes = {}
        messages.warning(request, 'Error al buscar informes.')
        grupos = Grupo.objects.all()

        context = {
            'informes': informes,
            'grupos': grupos,
            'informe_mensual': informe_mensual
        }

        return render(request, 'historico.html', context)

    grupos = Grupo.objects.all()

    context = {
        'informes': informes,
        'grupos': grupos,
        'informe_mensual': informe_mensual
    }

    return render(request, 'historico.html', context)


@login_required
def cambiar_estado_informe(request, id, grupo, estado):
    carro_informe = Carro_informe(request)
    carro_informe.cambiar_estado_informe(id, estado)
    request.session['grupo'] = request.POST.get("grupo", grupo)

    return redirect('nuevo_informe', id=grupo)
