from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Q, Sum
from django.utils import timezone
from datetime import datetime, timedelta
import json

# Importar tus modelos (ajusta según tu estructura)
from afiliaciones.models import Afiliacion, Solicitud, ArchivoSolicitud, Novedad
from salud.models import Eps, Regimen, SedeEPS, Municipio, Departamento, Empleador, SedeEPS 
from usuarios.models import Beneficiario, Usuario, Sisben, Documento
from django.contrib.auth.models import User
from django.http import FileResponse, Http404
import os



# Elimina import de SedeEPS, ya que no existe

@login_required
def dashboard(request):
    if request.method == 'GET':
  
       

        
        # 1️⃣ Totales básicos
        total_usuarios = Usuario.objects.count()
        total_afiliaciones = Afiliacion.objects.count()
        afiliaciones_activas = Afiliacion.objects.filter(estado='ACTIVO').count()
        afiliaciones_pendientes = Afiliacion.objects.filter(estado='EN TRAMITE').count()
        afiliaciones_mes = Afiliacion.objects.filter(
            fecha_afiliacion__gte=timezone.now().replace(day=1)
        ).count()

        # 2️⃣ Solicitudes
        total_solicitudes = Solicitud.objects.count()
        solicitudes_pendientes = Solicitud.objects.filter(estado='Pendiente').count()
        solicitudes_aprobadas = Solicitud.objects.filter(estado='Aprobado').count()
        solicitudes_rechazadas = Solicitud.objects.filter(estado='Rechazado').count()

        # 3️⃣ Novedades
        total_novedades = Novedad.objects.count()
        

        # 4️⃣ Querysets principales (para tablas)
        afiliaciones = Afiliacion.objects.select_related('usuario', 'eps', 'regimen', 'empleador').order_by('-fecha_afiliacion')
        solicitudes = Solicitud.objects.select_related('usuario').order_by('-fecha_solicitud')
        novedades = Novedad.objects.select_related('usuario').order_by('-fecha_novedad')
        total_sedes = SedeEPS.objects.count()
        total_departamentos = Departamento.objects.count()
        # 5️⃣ Municipios (solo si tienes la app de ubicaciones)
        municipios = Municipio.objects.all()

        # 6️⃣ Contexto final
        contexto = {
            'total_usuarios': total_usuarios,
            'total_afiliaciones': total_afiliaciones,
            'afiliaciones_activas': afiliaciones_activas,
            'afiliaciones_pendientes': afiliaciones_pendientes,
            'afiliaciones_mes': afiliaciones_mes,

            'total_solicitudes': total_solicitudes,
            'solicitudes_pendientes': solicitudes_pendientes,
            'solicitudes_aprobadas': solicitudes_aprobadas,
            'solicitudes_rechazadas': solicitudes_rechazadas,

            'total_novedades': total_novedades,
            'total_sedes': total_sedes,
            'total_departamentos': total_departamentos,
            'afiliaciones': afiliaciones,
            'solicitudes': solicitudes,
            'novedades': novedades,
            'municipios': municipios,
            'total_municipios': municipios.count(),
        }

        
        return render(request, 'dashboard.html', contexto)

from django.shortcuts import get_object_or_404

@login_required
def crear_afiliacion(request):
    """Crear nueva afiliación"""
    if request.method == 'POST':
        try:
            # Obtener los IDs enviados por el formulario
            usuario_id = request.POST.get('usuario_id')
            eps_id = request.POST.get('eps_id')
            regimen_id = request.POST.get('regimen_id')
            empleador_id = request.POST.get('empleador_id')
            fecha_afiliacion = request.POST.get('fecha_afiliacion')
            
            # Buscar las instancias reales (esto lanza 404 si no existen)
            usuario = get_object_or_404(Usuario, pk=usuario_id)
            eps = get_object_or_404(Eps, pk=eps_id)
            regimen = get_object_or_404(Regimen, pk=regimen_id)

            # Si empleador es opcional
            empleador = None
            if empleador_id:
                empleador = get_object_or_404(Empleador, pk=empleador_id)
            
            # Crear la afiliación con objetos, no IDs
            afiliacion = Afiliacion.objects.create(
                usuario=usuario,
                eps=eps,
                regimen=regimen,
                empleador=empleador,
                fecha_afiliacion=fecha_afiliacion,
                estado='ACTIVO',
            )

            messages.success(request, f'Afiliación {afiliacion.id} creada exitosamente')
            return redirect('dashboard')
            
        except Exception as e:
            messages.error(request, f'Error al crear la afiliación: {str(e)}')
            return redirect('crear_afiliacion')
    
    # GET - Mostrar formulario
    context = {
        'usuarios': Usuario.objects.all(),
        'eps_list': Eps.objects.all(),
        'regimenes': Regimen.objects.all(),
        'sedes_eps': SedeEPS.objects.select_related('eps', 'municipio').all(),
        'empleadores': Empleador.objects.all(),
    }
    return render(request, 'crear_afiliacion.html', context)

@login_required
def ver_afiliacion(request, afiliacion_id):
    """Ver detalles de una afiliación"""
    afiliacion = get_object_or_404(Afiliacion, id=afiliacion_id)
    usuario = afiliacion.usuario
    sisben = Sisben.objects.filter(usuario=usuario).first()
    
    # Obtener documentos del usuario
    documentos = Documento.objects.filter(usuario=usuario)
    
    # Para los selects de edición
    eps_list = Eps.objects.all()
    regimenes = Regimen.objects.all()
    empleadores = Empleador.objects.all()
    
    # Usuarios disponibles para agregar como beneficiarios (excluyendo los que ya son beneficiarios)
    beneficiarios_actuales = Beneficiario.objects.filter(usuario=usuario)
    ids_beneficiarios = beneficiarios_actuales.values_list('beneficiario_id', flat=True)
    usuarios_disponibles = Usuario.objects.exclude(id__in=ids_beneficiarios).exclude(id=usuario.id)
    
    context = {
        'afiliacion': afiliacion,
        'beneficiarios': beneficiarios_actuales,
        'sisben': sisben,
        'documentos': documentos,
        'eps_list': eps_list,
        'regimenes': regimenes,
        'empleadores': empleadores,
        'usuarios_disponibles': usuarios_disponibles,
    }
    return render(request, 'detalle_afiliacion.html', context)
@login_required
def descargar_documento(request, documento_id):
    """Descargar un documento"""
    documento = get_object_or_404(Documento, id=documento_id)
    
    try:
        # Obtener la ruta del archivo
        file_path = documento.archivo.path
        
        # Verificar que el archivo existe
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
        else:
            messages.error(request, 'Archivo no encontrado')
            return redirect(request.META.get('HTTP_REFERER', 'dashboard'))
    except Exception as e:
        messages.error(request, f'Error al descargar: {str(e)}')
        return redirect(request.META.get('HTTP_REFERER', 'dashboard'))



@login_required
def editar_afiliacion(request, afiliacion_id):
    """Editar una afiliación existente"""
    afiliacion = get_object_or_404(Afiliacion, id=afiliacion_id)
    
    if request.method == 'POST':
        try:
            afiliacion.eps_id = request.POST.get('eps_id')
            afiliacion.regimen_id = request.POST.get('regimen_id')
            afiliacion.empleador_id = request.POST.get('empleador_id') or None
            afiliacion.estado = request.POST.get('estado')
            afiliacion.save()
            
            messages.success(request, 'Afiliación actualizada exitosamente')
            return redirect('ver_afiliacion', afiliacion_id=afiliacion.id)
            
        except Exception as e:
            messages.error(request, f'Error al actualizar: {str(e)}')
    
    # Si es GET, redirigir a la vista de detalle
    return redirect('ver_afiliacion', afiliacion_id=afiliacion.id)

@login_required
def agregar_beneficiario(request, afiliacion_id):
    """Agregar beneficiario a una afiliación"""
    afiliacion = get_object_or_404(Afiliacion, id=afiliacion_id)
    
    if request.method == 'POST':
        try:
            # Obtener el usuario beneficiario (debe existir previamente)
            beneficiario_id = request.POST.get('beneficiario_id')
            parentesco = request.POST.get('parentesco')
            
            beneficiario_usuario = get_object_or_404(Usuario, id=beneficiario_id)
            
            Beneficiario.objects.create(
                usuario=afiliacion.usuario,
                beneficiario=beneficiario_usuario,
                parentesco=parentesco
            )
            
            messages.success(request, 'Beneficiario agregado exitosamente')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return redirect('ver_afiliacion', afiliacion_id=afiliacion.id)

@login_required
def eliminar_beneficiario(request, beneficiario_id):
    """Eliminar un beneficiario"""
    beneficiario = get_object_or_404(Beneficiario, id=beneficiario_id)
    usuario = beneficiario.usuario
    afiliacion = Afiliacion.objects.filter(usuario=usuario).first()
    
    if request.method == 'POST':
        beneficiario.delete()
        messages.success(request, 'Beneficiario eliminado exitosamente')
    
    return redirect('ver_afiliacion', afiliacion_id=afiliacion.id)

@login_required
def ver_solicitud(request, solicitud_id):
    """Ver detalles de una solicitud"""
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)
    
    # Obtener archivos de la solicitud
    archivos = ArchivoSolicitud.objects.filter(solicitud=solicitud)
    
    context = {
        'solicitud': solicitud,
        'archivos': archivos,  # ← Ya lo tenías, perfecto
    }
    return render(request, 'detalle_solicitudes.html', context)

@login_required
def agregar_documento(request, afiliacion_id):
    """Agregar documento a un usuario"""
    afiliacion = get_object_or_404(Afiliacion, id=afiliacion_id)
    
    if request.method == 'POST':
        try:
            tipo = request.POST.get('tipo')
            archivo = request.FILES.get('archivo')
            
            if archivo:
                Documento.objects.create(
                    usuario=afiliacion.usuario,
                    tipo=tipo,
                    archivo=archivo
                )
                messages.success(request, 'Documento agregado exitosamente')
            else:
                messages.error(request, 'Debe seleccionar un archivo')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return redirect('ver_afiliacion', afiliacion_id=afiliacion.id)

@login_required
def eliminar_documento(request, documento_id):
    """Eliminar un documento"""
    documento = get_object_or_404(Documento, id=documento_id)
    usuario = documento.usuario
    afiliacion = Afiliacion.objects.filter(usuario=usuario).first()
    
    if request.method == 'POST':
        # Eliminar archivo físico
        if documento.archivo:
            try:
                os.remove(documento.archivo.path)
            except:
                pass
        
        documento.delete()
        messages.success(request, 'Documento eliminado exitosamente')
    
    return redirect('ver_afiliacion', afiliacion_id=afiliacion.id)
@login_required
def aprobar_solicitud(request, solicitud_id):
    """Aprobar una solicitud"""
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)
    
    if request.method == 'POST':
        solicitud.estado = 'Aprobado'  # ← Usa el mismo valor que en tu BD
        solicitud.save()
        
        messages.success(request, 'Solicitud aprobada exitosamente')
        return redirect('ver_solicitud', solicitud_id=solicitud.id)
    
    return redirect('dashboard')


@login_required
def rechazar_solicitud(request, solicitud_id):
    """Rechazar una solicitud"""
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)
    
    if request.method == 'POST':
        observacion = request.POST.get('observacion', '')
        solicitud.estado = 'Rechazado'  # ← Usa el mismo valor que en tu BD
        solicitud.observacion = observacion
        solicitud.save()
        
        messages.warning(request, 'Solicitud rechazada')
        return redirect('ver_solicitud', solicitud_id=solicitud.id)
    
    return redirect('dashboard')

@login_required
def descargar_archivo_solicitud(request, archivo_id):
    """Descargar archivo de solicitud"""
    archivo_solicitud = get_object_or_404(ArchivoSolicitud, id=archivo_id)
    
    try:
        file_path = archivo_solicitud.archivo.path
        
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
        else:
            messages.error(request, 'Archivo no encontrado')
            return redirect(request.META.get('HTTP_REFERER', 'dashboard'))
    except Exception as e:
        messages.error(request, f'Error al descargar: {str(e)}')
        return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

@login_required
def crear_novedad(request):
    """Crear nueva novedad"""
    if request.method == 'POST':
        try:
            usuario_id = request.POST.get('usuario_id')
            
            descripcion = request.POST.get('descripcion')
            fecha_novedad = request.POST.get('fecha_novedad') or timezone.now()

            # Buscar el usuario en tu modelo Usuario
            usuario = Usuario.objects.get(id=usuario_id)
            
            Novedad.objects.create(
                usuario=usuario,
             
                descripcion=descripcion,
                fecha_novedad=fecha_novedad
            )
            
            messages.success(request, 'Novedad registrada exitosamente')
            return redirect('dashboard')
            
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario no encontrado')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    context = {
        'usuarios': Usuario.objects.all(),  # Usamos tu modelo Usuario
    }
    return render(request, 'crear_novedad.html', context)


@login_required
def ver_novedad(request, novedad_id):
    """Ver detalles de una novedad"""
    novedad = get_object_or_404(Novedad, id=novedad_id)
    return render(request, 'detalle_novedad.html', {'novedad': novedad})


@login_required
def editar_novedad(request, novedad_id):
    """Editar una novedad"""
    novedad = get_object_or_404(Novedad, id=novedad_id)
    
    if request.method == 'POST':
        novedad.tipo = request.POST.get('tipo')
        novedad.descripcion = request.POST.get('descripcion')
        novedad.save()
        
        messages.success(request, 'Novedad actualizada')
        return redirect('ver_novedad', novedad_id=novedad.id)
    
    return render(request, 'editar_novedad.html', {'novedad': novedad})


@login_required
def estadisticas_municipios(request):
    """Estadísticas detalladas por municipio"""
    
    municipios_stats = []
    
    for municipio in Municipio.objects.all():
        # Contar sedes
        total_sedes = SedeEPS.objects.filter(municipio=municipio).count()
        
        # Contar afiliados por sedes en ese municipio
        total_afiliados = Afiliacion.objects.filter(
            municipio=municipio,
            estado='ACTIVO'
        ).count()
        
        # Contar traslados
        
        
        # Contar solicitudes pendientes
        
        
        municipios_stats.append({
            'municipio': municipio,
            'total_sedes': total_sedes,
            'total_afiliados': total_afiliados,
           
           
        })
    
    context = {
        'municipios_stats': municipios_stats
    }
    return render(request, 'estadistica_municipio.html', context)


@login_required
def reportes_ia(request):
    """Generación de reportes con análisis básico"""
    
    # Datos para análisis
    total_afiliaciones = Afiliacion.objects.count()
    afiliaciones_activas = Afiliacion.objects.filter(estado='ACTIVO').count()
    
    # Tendencia mensual (últimos 6 meses)
    meses_data = []
    for i in range(6):
        fecha = timezone.now() - timedelta(days=30*i)
        inicio_mes = fecha.replace(day=1)
        fin_mes = (inicio_mes + timedelta(days=32)).replace(day=1)
        
        count = Afiliacion.objects.filter(
            fecha_afiliacion__gte=inicio_mes,
            fecha_afiliacion__lt=fin_mes
        ).count()
        
        meses_data.append({
            'mes': inicio_mes.strftime('%B %Y'),
            'afiliaciones': count
        })
    
    # Distribución por régimen
    regimenes_data = Regimen.objects.annotate(
    total=Count('afiliacion')
).values('tipo_regimen', 'porcentaje_cotizacion', 'total')
    
    # Análisis simple (sin IA real, pero estructura preparada)
    analisis = {
        'tendencia': 'Crecimiento sostenido' if meses_data[0]['afiliaciones'] > meses_data[-1]['afiliaciones'] else 'Decrecimiento',
        'tasa_activacion': round((afiliaciones_activas / total_afiliaciones * 100), 2) if total_afiliaciones > 0 else 0,
        'recomendaciones': [
            'Incrementar campañas de afiliación en municipios con baja cobertura',
            'Agilizar el proceso de aprobación de solicitudes pendientes',
            'Implementar seguimiento a novedades de traslado'
        ]
    }
    
    context = {
        'total_afiliaciones': total_afiliaciones,
        'afiliaciones_activas': afiliaciones_activas,
        'meses_data': json.dumps(meses_data),
        'regimenes_data': list(regimenes_data),
        'analisis': analisis,
    }
    
    return render(request, 'reportes_ia.html', context)


@login_required
def obtener_sedes_por_eps(request):
    """API para obtener sedes según EPS seleccionada"""
    eps_id = request.GET.get('eps_id')
    sedes = SedeEPS.objects.filter(eps_id=eps_id).values('id', 'nombre', 'municipio__nombre')
    return JsonResponse(list(sedes), safe=False)


@login_required
def historial_usuario(request, usuario_id):
    afiliacion = Afiliacion.objects.filter(usuario=usuario_id).first()
    usuario = afiliacion.usuario

    novedades = Novedad.objects.filter(usuario=usuario).order_by('-fecha_novedad')

    context = {
        'usuario': usuario,
        'afiliacion': afiliacion,   # ← IMPORTANTE
        'novedades': novedades,
        'total_novedades': novedades.count(),
    }

    return render(request, 'historial_usuario.html', context)