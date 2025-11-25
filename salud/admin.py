from django.contrib import admin
from .models import Empresa_Aportante, SedeEmpresaAprotante, Empleador, Regimen, Eps, Departamento, Municipio, SedeEPS, AdministradorEPS

class EmpresaAportanteAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

class SedeEmpresaAportanteAdmin(admin.ModelAdmin):
    list_display = ('empresa__nombre', 'direccion', 'telefono', 'email', 'municipio')

class EmpleadorAdmin(admin.ModelAdmin):
    list_display = ('user__first_name', 'user__last_name' ,'tipo_documento', 'numero_documento', 'fecha_nacimiento', 'empresa_aportante')

class RegimenAdmin(admin.ModelAdmin):
    list_display = ('tipo_regimen', 'fuente_cotizacion', 'porcentaje_cotizacion')

class EpsAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'nit')

class AdministradorEPSAdmin(admin.ModelAdmin):
    list_display = ('user__first_name', 'user__last_name', 'tipo_documento', 'numero_documento', 'eps__nombre')

class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo_dane')

class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'departamento__nombre', 'codigo_dane')

class SedeEpsAdmin(admin.ModelAdmin):
    list_display = ('eps__nombre', 'municipio__nombre', 'direccion', 'telefono', 'email')



admin.site.register(Empresa_Aportante, EmpresaAportanteAdmin)
admin.site.register(SedeEmpresaAprotante, SedeEmpresaAportanteAdmin)    
admin.site.register(Empleador, EmpleadorAdmin)
admin.site.register(Regimen, RegimenAdmin)
admin.site.register(Eps, EpsAdmin)
admin.site.register(AdministradorEPS, AdministradorEPSAdmin)
admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Municipio, MunicipioAdmin)
admin.site.register(SedeEPS, SedeEpsAdmin)


