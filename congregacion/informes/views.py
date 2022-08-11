from django.shortcuts import render

from admin_congregacion.models import Grupo

# Create your views here.
def index(request):
    return render(request, 'index.html')
    