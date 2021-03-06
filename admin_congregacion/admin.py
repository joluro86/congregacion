from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from admin_congregacion.models import *

class PublicadorResource(resources.ModelResource):
    class Meta:
        model = Publicador

class CongregacionAdmin(admin.ModelAdmin):
    list_display = ('numero', 'nombre', 'municipio')
admin.site.register(Congregacion, CongregacionAdmin)

class SuperintendenteAdmin(admin.ModelAdmin):
    list_display = ('id','nombre',)
admin.site.register(Superintendente, SuperintendenteAdmin)

class GrupoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'superintendente', 'congregacion')
admin.site.register(Grupo, GrupoAdmin)

class Tipo_publicadorAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo')
admin.site.register(Tipo_publicador, Tipo_publicadorAdmin)

class EstadoPublicadorAdmin(admin.ModelAdmin):
    list_display = ('id', 'estado')
admin.site.register(EstadoPublicador, EstadoPublicadorAdmin)

class PrecursoradoAdmin(admin.ModelAdmin):
    list_display = ('id', 'precursorado')
admin.site.register(Precursorado, PrecursoradoAdmin)

class PublicadorAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'nombre', 'grupo', 'tipo', 'sexo', 'precursor', 'estado')
admin.site.register(Publicador, PublicadorAdmin)


