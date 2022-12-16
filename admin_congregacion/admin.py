from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from admin_congregacion.models import *

class PivoteUserToSuperintendenteResource(resources.ModelResource):
    class Meta:
        model = PivoteUserToSuperintendente

class PublicadorResource(resources.ModelResource):
    class Meta:
        model = Publicador

class PublicadorInactivoResource(resources.ModelResource):
    class Meta:
        model = PublicadorInactivo

class GrupoResource(resources.ModelResource):
    class Meta:
        model = Grupo

class PublicadorIrregularResource(resources.ModelResource):
    class Meta:
        model = PublicadorIrregular

class PivoteUserToSuperintendenteAdmin(admin.ModelAdmin):
    list_display = ('superintendente', 'grupo', 'user')

class CongregacionAdmin(admin.ModelAdmin):
    list_display = ('numero', 'nombre', 'municipio')
admin.site.register(Congregacion, CongregacionAdmin)

class GrupoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('numero', 'superintendente', 'congregacion')
admin.site.register(Grupo, GrupoAdmin)

class SuperintendenteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'nombre')
admin.site.register(Superintendente, SuperintendenteAdmin)

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

admin.site.register(PivoteUserToSuperintendente, PivoteUserToSuperintendenteAdmin)

class PublicadorInactivoAdmin(admin.ModelAdmin):
    list_display = ('id', 'publicador')
admin.site.register(PublicadorInactivo, PublicadorInactivoAdmin)

class PublicadorIrregularAdmin(admin.ModelAdmin):
    list_display = ('id', 'publicador')
admin.site.register(PublicadorIrregular, PublicadorIrregularAdmin)




