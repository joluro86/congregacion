from informes.views import *
from django.urls import path

urlpatterns = [
    path('', index, name="index"),
    path('nuevo_informe/<int:id>/', nuevo_informe , name="nuevo_informe"),
    path('guardar_informe_publicador/<int:id>/', guardar_informe_grupo , name="guardar_informe_publicador"),   
    path('finalizar_informe/<int:id>/', finalizar_informe , name="finalizar_informe"), 
    path('cancelar_informe/', cancelar_informe, name="cancelar_informe"), 
    path('informe_actual/', Crear_Informe_Actual, name="informe_actual"), 
    path('informes/', InformeMensualList.as_view(), name="informes_mensuales_list"), 
    path('informes_publicador/<int:id>/', lista_informes_publicador, name="informes_publicador"), 
    path('cambiar_estado_informe/<int:id>/<int:grupo>/<int:estado>/', cambiar_estado_informe, name="cambiar_estado_informe"),
    path('busqueda_informe_mensual/<int:id>/', busqueda_informe_mensual, name="busqueda_informe_mensual"), 
    path('busqueda_informe_mensual_grupo/<int:id>/', busqueda_informe_mensual_id_grupo, name="busqueda_informe_mensual_id_grupo"), 
]
