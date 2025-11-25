from django.db import models
from usuarios.models import Usuario
from salud.models import Eps, Regimen, Empleador, Municipio
# Create your models here.

ESTADO =[
    ('Pendiente', 'Pendiente'),
    ('Aprobado', 'Aprobado'),
    ('Rechazado', 'Rechazado'),
]

TIPO_SOLICITUD = [
    
    ('Cambio de EPS', 'Cambio de EPS'),
    ('Actualizacion de Datos', 'Actualizacion de Datos'),

]

ESTADO_AFILIACION = [
    ('ACTIVO', 'ACTIVO'),
    ('EN TRAMITE', 'EN TRAMITE'),
    ('INACTIVO', 'INACTIVO'),
]
class Afiliacion(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    eps = models.ForeignKey(Eps, on_delete=models.CASCADE)
    regimen = models.ForeignKey(Regimen, on_delete=models.CASCADE)
    empleador = models.ForeignKey(Empleador, on_delete=models.CASCADE, null=True, blank=True)
    fecha_afiliacion = models.DateField(auto_now_add=True)
    estado = models.CharField(choices=ESTADO_AFILIACION, max_length=50, default='ACTIVO')
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"Afiliacion de {self.usuario.user.first_name} a {self.eps.nombre}"

class Solicitud(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)
    estado = models.CharField(choices=ESTADO, max_length=50, default='Pendiente')
    fecha_solicitud = models.DateField(auto_now_add=True)
    tipo_solicitud = models.CharField(choices=TIPO_SOLICITUD, max_length=50)
    observaciones = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"Solicitud de {self.usuario.user.first_name} {self.usuario.user.last_name} - Estado: {self.estado}"

class ArchivoSolicitud(models.Model):
    tipo = models.CharField(max_length=100)
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='solicitudes/')
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return f"Archivo de {self.solicitud.usuario.user.first_name} - {self.archivo.name}"

class Novedad(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    descripcion = models.TextField()
    fecha_novedad = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Novedad de {self.afiliacion.usuario.user.first_name} - {self.fecha_novedad}"