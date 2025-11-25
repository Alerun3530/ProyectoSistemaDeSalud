from django.urls import path
from . import views

urlpatterns = [
    # Afiliaciones (el prefijo 'afiliaciones/' ya viene del urls.py principal)
    path('dashboard/', views.dashboard, name='dashboard'),
    path('crear/', views.crear_afiliacion, name='crear_afiliacion'),
    path('<int:afiliacion_id>/', views.ver_afiliacion, name='ver_afiliacion'),
    path('<int:afiliacion_id>/editar/', views.editar_afiliacion, name='editar_afiliacion'),
    path('afiliaciones/<int:afiliacion_id>/beneficiarios/agregar/', views.agregar_beneficiario, name='agregar_beneficiario'),
    path('beneficiarios/<int:beneficiario_id>/eliminar/', views.eliminar_beneficiario, name='eliminar_beneficiario'),
    path('afiliaciones/<int:afiliacion_id>/documentos/agregar/', views.agregar_documento, name='agregar_documento'),
    path('documentos/<int:documento_id>/eliminar/', views.eliminar_documento, name='eliminar_documento'),
    
    # Solicitudes
    path('solicitudes/<int:solicitud_id>/', views.ver_solicitud, name='ver_solicitud'),
    path('solicitudes/<int:solicitud_id>/aprobar/', views.aprobar_solicitud, name='aprobar_solicitud'),
    path('solicitudes/<int:solicitud_id>/rechazar/', views.rechazar_solicitud, name='rechazar_solicitud'),
    path('documentos/<int:documento_id>/descargar/', views.descargar_documento, name='descargar_documento'),
    path('archivos-solicitud/<int:archivo_id>/descargar/', views.descargar_archivo_solicitud, name='descargar_archivo_solicitud'),
    # Novedades
    path('novedades/crear/', views.crear_novedad, name='crear_novedad'),
    path('novedades/<int:novedad_id>/', views.ver_novedad, name='ver_novedad'),
    path('novedades/<int:novedad_id>/editar/', views.editar_novedad, name='editar_novedad'),
    path('usuarios/<int:usuario_id>/historial/', views.historial_usuario, name='historial_usuario')
,
    
    # Municipios
    path('municipios/estadisticas/', views.estadisticas_municipios, name='estadisticas_municipios'),
    
    # Reportes
    path('reportes/ia/', views.reportes_ia, name='reportes_ia'),
    
    # API auxiliar
    path('api/sedes-por-eps/', views.obtener_sedes_por_eps, name='api_sedes_por_eps'),
]