from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from admin_congregacion.models import Grupo, Publicador
from informes.carro_informe_grupo import Carro_informe
from informes.forms import InfomeMensualForm
from informes.models import EstadoInforme, InformeMensual, InformePublicador, PivoteInformeMensualGrupo
from django.views.generic import ListView, UpdateView, CreateView

def index(request):
    return render(request, 'index.html')

def Crear_Informe_Actual(request):

    if (request.method == 'POST'):
        informes_abiertos= InformeMensual.objects.filter(estado='1')
        if len(informes_abiertos)==0:
            formset = InfomeMensualForm(request.POST)
            if formset.is_valid():
                formset.save()
        else:
            formset = InfomeMensualForm(request.POST)
            messages.warning(request, 'No se pudo crear este registro debido a que existen informes pendientes por cerrar.')
            return render(request, 'informe_Actual.html', {'form': formset})

    formset = InfomeMensualForm()
    return render(request, 'informe_Actual.html', {'form': formset})

def validar_pivote_informe_grupo(grupo, mes):
    informes = PivoteInformeMensualGrupo.objects.filter(grupo=grupo).filter(informe_mensual=mes)
    if len(informes)>0:
        return True
    
def nuevo_informe(request, id):

    informes_abiertos= InformeMensual.objects.filter(estado='1')
    grupo= Grupo.objects.get(numero=id)

    if len(Publicador.objects.filter(grupo=grupo))<1:
        print("sin publicadores" + str(id))
        messages.warning(request, 'Registre publicadores en este grupo para enviar informes.')
        return redirect('publicadores_por_grupo', id)

    for i in informes_abiertos:
        inf_mes= i
    
    try:
        if validar_pivote_informe_grupo(grupo, inf_mes):
            messages.warning(request, 'El informe de este grupo ya fue ingresado.')
            return redirect('publicadores_por_grupo', id)
    except:
        pass

    if len(informes_abiertos)==0:       
        messages.warning(request, 'No existen informes pendientes. Comuniquese con el administrador.')
        return redirect('grupos')
    elif len(informes_abiertos)>1:
        messages.warning(request, 'Existe mas de un informe pendiente. Habilite solo uno.')
        return redirect('grupos')
    else:
        publicadores = Publicador.objects.filter(grupo=grupo) 
        if len(publicadores)<1:
            messages.warning(request, 'Debe registrar publicadores en este grupo.')
            return redirect('grupos')
        try:
            grupo_informe= request.session.get('grupo')
            print("entre try")
        except:
            print("entre except")
            grupo_informe= request.session.get('grupo', '0')
        finally:
            
            if str(grupo_informe) != str(id):
                limpiar_carro(request)

        carro = Carro_informe(request)
        for p in publicadores:
            carro.agregar(p)

    for i in informes_abiertos:
        inf_mes= i

    return render(request, 'nuevo_informe.html', {'grupo':grupo, 'informe_mensual': inf_mes})

def guardar_informe_grupo(request, id):
    if request.method == "POST":
        id_publicador=request.POST.get("id")
        p=request.POST.get("pub")
        v=request.POST.get("vid")
        h=request.POST.get("hor")
        r=request.POST.get("rev")
        c=request.POST.get("cur")
        o=request.POST.get("obs")

        carro_informe = Carro_informe(request)
        carro_informe.cambiar_cantidad_informe(id_publicador, p, v, h, r, c, o)
        request.session['grupo']= request.POST.get("grupo")
    return redirect('nuevo_informe', id=id)

def finalizar_informe(request, id):

    try:
        mes_informe = InformeMensual.objects.all()
        mes=''
        for m in mes_informe:
            
            if str(m.estado)=='Abierto':
                mes= m   

        for key, value in request.session.get("carro").items():   
            inf = InformePublicador()
            inf.informe_mensual = mes
            inf.publicador = Publicador.objects.get(id=value['id']) 
            inf.publicaciones = value['publicaciones']
            inf.videos = value['videos']
            inf.horas = value['horas']
            inf.revisitas = value['revisitas']
            inf.cursos = value['cursos']
            inf.observaciones = value['observaciones']
            inf.estado = EstadoInforme.objects.get(estado='Abierto')
            inf.save()

        pivote_informe_grupo = PivoteInformeMensualGrupo()
        pivote_informe_grupo.grupo = Grupo.objects.get(numero=id)
        pivote_informe_grupo.informe_mensual = mes
        pivote_informe_grupo.save()

        limpiar_carro(request)

        messages.warning(request, 'Informe guardado con existo.')

    except:
        messages.warning(request, 'El informe no pudo ser creado.')

    return redirect('publicadores_por_grupo', id)

def limpiar_carro(request):
    request.session['carro']={}
    request.session.modified=True

def cancelar_informe(request):
    limpiar_carro(request)
    return redirect('grupos')
        
class InformeMensualList(ListView):
    #login_url = 'login'
    model = InformeMensual
    template_name= "list_informes_mensuales.html"

def lista_informes_publicador(request, id):
    try:
        publicador = Publicador.objects.get(id=id)
        informes= InformePublicador.objects.filter(publicador=publicador)

        if len(informes)<1:
            print(len(informes))
            messages.warning(request, 'Publicador no tiene informes registrados.')
            return redirect('publicadores_por_grupo', publicador.grupo.numero)
        else:
            return render(request, 'lista_informes_publicador.html', { 'informes':informes, 'publicador':publicador })

    except:
        messages.warning(request, 'Publicador no tiene informes registrados.')
        return redirect('grupos')

def busqueda_informe_mensual(request, id):
    
    try:
        request.session['informe_mensual']={}
        request.session.modified=True

        informe_mensual=InformeMensual.objects.get(id=id)
        request.session['informe_mensual']= informe_mensual.id

        informes = InformePublicador.objects.filter(informe_mensual=informe_mensual)
    except:
        informes={}

    grupos = Grupo.objects.all()

    context = {
        'informes':informes,
        'grupos':grupos,
        'informe_mensual':informe_mensual
        }

    return render(request, 'historico.html', context)

def busqueda_informe_mensual_id_grupo(request, id):
    
    try:
        informe_mensual = InformeMensual.objects.get(id=request.session['informe_mensual'])
        grupo = Grupo.objects.get(numero=id)
        publicadores = Publicador.objects.filter(grupo=grupo)
        informes=[]
        for p in publicadores:
            print(p)
            informes.append(InformePublicador.objects.get(publicador=p))
    except:
        print("errrorrrrr")
        informes = {}

    grupos = Grupo.objects.all()

    context = {
        'informes':informes,
        'grupos':grupos,
        'informe_mensual':informe_mensual
        }

    return render(request, 'historico.html', context)

    



