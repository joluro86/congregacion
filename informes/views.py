from django.shortcuts import render

from admin_congregacion.models import Grupo, Publicador
from informes.carroinforme import Carro_informe

# Create your views here.

def limpiar_carro(request):
      carro = Carro_informe(request)
      carro.limpiar_carro()

def index(request):
    return render(request, 'index.html')

def nuevo_informe(request, id):

    limpiar_carro(request)  
      
    grupo= Grupo.objects.get(numero=id)
    publicadores = Publicador.objects.filter(grupo=grupo)

    carro_informe = Carro_informe(request)
    carro_informe.nuevo_informe(publicadores)       

    return render(request, 'nuevo_informe.html',{'grupo':grupo} )


    