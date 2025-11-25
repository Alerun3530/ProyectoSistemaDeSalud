from django.contrib import admin
from .models import Usuario, Documento, Sisben, Beneficiario

# Register your models here.
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('user__first_name','user__last_name','tipo_documento', 'numero_documento', 'fecha_nacimiento')


class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('usuario__user__first_name', 'usuario__user__last_name', 'tipo', 'archivo')

class SisbenAdmin(admin.ModelAdmin):
    list_display = ('usuario__user__first_name', 'usuario__user__last_name', 'clasificacion', 'fecha_actualizacion')

class BeneficiarioAdmin(admin.ModelAdmin):
    list_display = ('usuario__user__first_name', 'usuario__user__last_name', 'parentesco', 'fecha_nacimiento')


# Registrar los modelos en el admin
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Documento, DocumentoAdmin)
admin.site.register(Sisben, SisbenAdmin)
admin.site.register(Beneficiario, BeneficiarioAdmin)