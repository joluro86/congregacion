from django.shortcuts import render, redirect
from django.contrib import messages
from admin_congregacion.models import Grupo, Publicador
from informes.carro_informe_grupo import Carro_informe
from informes.forms import InfomeMensualForm
from informes.models import InformeMensual, InformePublicador

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

def nuevo_informe(request, id):

    informes_abiertos= InformeMensual.objects.filter(estado='1')
    grupo= Grupo.objects.get(numero=id)
    print(len(informes_abiertos))
    if len(informes_abiertos)==0:       
        messages.warning(request, 'No se pueden registrar informes. Comuniquese con el administrador.')
        return redirect('grupos')
    else:
        publicadores = Publicador.objects.filter(grupo=grupo) 

        try:
            grupo_informe= request.session.get('grupo')
            print("entre try")
        except:
            print("entre except")
            grupo_informe= request.session.get('grupo', '0')
        finally:
            
            if str(grupo_informe) != str(id):
                print("grupo inf: "+ str(grupo_informe)+ " id: "+str(id))
                limpiar_carro(request)

        carro = Carro_informe(request)
        for p in publicadores:
            carro.agregar(p)
            print(p)

    return render(request, 'nuevo_informe.html',{'grupo':grupo} )

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
        print("grupo: " + str(request.POST.get("grupo")))
        request.session['grupo']= request.POST.get("grupo")
    return redirect('nuevo_informe', id=id)

def finalizar_informe(request):

    mes_informe = InformeMensual.objects.all()
    mes=''
    for m in mes_informe:
        if str(m.estado)=='1':
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
        inf.save()
    
    limpiar_carro(request)
    
    return render(request, 'index.html')

def limpiar_carro(request):
    request.session['carro']={}
    request.session.modified=True

def cancelar_informe(request):
    limpiar_carro(request)
    return redirect('grupos')
        

    