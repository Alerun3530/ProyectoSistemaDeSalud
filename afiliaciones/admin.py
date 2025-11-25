from django.contrib import admin
from .models import Afiliacion, Solicitud, ArchivoSolicitud, Novedad
# Register your models here.
class AfiliacionAdmin(admin.ModelAdmin):
    list_display = ('usuario__user__first_name', 'usuario__user__last_name', 'usuario__numero_documento','eps__nombre', 'regimen__tipo_regimen', 'empleador__user__first_name', 'fecha_afiliacion')

class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('usuario__user__first_name', 'usuario__user__last_name', 'descripcion', 'estado', 'fecha_solicitud', 'tipo_solicitud')

class ArchivoSolicitudAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'solicitud__usuario__user__first_name', 'solicitud__usuario__user__last_name', 'archivo')

class NovedadAdmin(admin.ModelAdmin):
    list_display = ('usuario__user__first_name', 'usuario__user__last_name', 'descripcion', 'fecha_novedad')

admin.site.register(Afiliacion, AfiliacionAdmin)
admin.site.register(Solicitud, SolicitudAdmin)
admin.site.register(ArchivoSolicitud, ArchivoSolicitudAdmin)
admin.site.register(Novedad, NovedadAdmin)


    