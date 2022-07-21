from django.contrib import admin

from informes.models import *

# Register your models here.

class InformeMensualAdmin(admin.ModelAdmin):
    list_display = ('id', 'mes', 'año', 'estado')

admin.site.register(InformeMensual, InformeMensualAdmin)

