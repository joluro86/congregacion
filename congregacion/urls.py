"""congregacion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from admin_congregacion.views import *

urlpatterns = [
    path('', include('informes.urls')),
    path('admin/', admin.site.urls),
    path('publicadores/<int:id>/', publicadores_por_grupo, name="publicadores_por_grupo"),
    path('grupos/', grupos, name="grupos"),
    path('nuevo_publicador/', Crear_Publicador.as_view(), name="nuevo_publicador")
]
