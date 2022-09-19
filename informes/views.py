from django.shortcuts import render, redirect

from admin_congregacion.models import Grupo, Publicador
from informes.carro_informe_grupo import Carro_informe
from informes.models import InformeMensual, InformePublicador


def index(request):
    return render(request, 'index.html')

def grupo_id(self):
    return int(self.id)

def nuevo_informe(request, id):       
    grupo= Grupo.objects.get(numero=id)
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
        

    