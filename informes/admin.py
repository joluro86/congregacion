from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from informes.models import *

# Register your models here.

class AñoResource(resources.ModelResource):
    class Meta:
        model = Año

class AñoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

class EstadoInformeResource(resources.ModelResource):
    class Meta:
        model = EstadoInforme

class EstadoInformeAdmin(admin.ModelAdmin):
    list_display = ('id', 'estado')

class InformePublicadorResource(resources.ModelResource):
    class Meta:
        model = InformePublicador
        
class InformeMensualAdmin(admin.ModelAdmin):
    list_display = ('id', 'mes', 'año', 'estado')

admin.site.register(InformeMensual, InformeMensualAdmin)

class InformePublicadorAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('informe_mensual', 'publicador', 'publicaciones', 'videos', 'horas', 'revisitas', 'cursos', 'observaciones', 'estado')

admin.site.register(InformePublicador, InformePublicadorAdmin)
admin.site.register(Año, AñoAdmin)
admin.site.register(EstadoInforme, EstadoInformeAdmin)


