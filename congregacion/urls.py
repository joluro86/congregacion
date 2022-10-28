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
    path('', include('User.urls')),
    path('admin/', admin.site.urls),
    path('publicadores/<int:id>/', publicadores_por_grupo, name="publicadores_por_grupo"),
    path('publicadores_congregacion/', publicadores_congregacion, name='publicadores_congregacion'),
    path('calculo_inactivos/', calculo_inactivos, name="calculo_inactivos"),
    path('publicadores_inactivos/', publicadores_inactivos, name="publicadores_inactivos"),
    path('calculo_irregulares/', calculo_irregulares, name="calculo_irregulares"),
    path('publicadores_irregulares/', publicadores_irregulares, name="publicadores_irregulares"),
    path('grupos/', grupos, name="grupos"),
    path('ancianos/', ancianos, name="ancianos"),
    path('ministeriales/', ministeriales, name="ministeriales"),
    path('accounts/', include('django.contrib.auth.urls'))
]
