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

from informes.views import *
from django.urls import include, path

urlpatterns = [
    path('index/', index, name="index"),
    path('nuevo_informe/<int:id>/', nuevo_informe , name="nuevo_informe"),
    path('guardar_informe_publicador/<int:id>/', guardar_informe_grupo , name="guardar_informe_publicador"),    
]
