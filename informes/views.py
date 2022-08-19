from django.shortcuts import render, redirect

from admin_congregacion.models import Grupo, Publicador
from informes.carro_informe_grupo import Carro_informe

def limpiar_carro(request):
      carro = Carro_informe(request)
      carro.limpiar_carro()

def index(request):
    return render(request, 'index.html')

def grupo_id(self):
    return int(self.id)

def nuevo_informe(request, id):       
    grupo= Grupo.objects.get(numero=id)
    publicadores = Publicador.objects.filter(grupo=grupo)  
    carro = Carro_informe(request)
    request.session['grupo'] = 100
    i= request.session.get('grupo')
    print(i)
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
        
    return redirect('nuevo_informe', id=id)
        

    