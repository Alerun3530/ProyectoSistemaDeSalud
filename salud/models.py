from django.db import models
from usuarios.models import Usuario
from django.contrib.auth.models import User
# Create your models here.
TIPO_REGIMEN_CHOICES = [
    ('Contributivo', 'Contributivo'),
    ('Subsidiado', 'Subsidiado'),
    ]

TIPO_EPS_CHOICES = [
    ('Publica', 'Publica'),
    ('Privada', 'Privada'),
    ('Mixta', 'Mixta'),
    ]
TIPO_DOCUMENTO_CHOICES = [
    ('CC', 'Cedula de Ciudadania'), 
    ('TI', 'Tarjeta de Identidad'), 
    ('CE', 'Cedula de Extranjeria'), 
    ('PP', 'Pasaporte')]



class Empresa_Aportante(models.Model):
    nombre = models.CharField(max_length=200)
    
    

    def __str__(self):
        return self.nombre
class SedeEmpresaAprotante(models.Model):
    empresa = models.ForeignKey(Empresa_Aportante, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=300)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    municipio = models.CharField(max_length=100)

    def __str__(self):
        return f"Sede de {self.empresa.nombre} - {self.direccion}"

class Empleador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_documento = models.CharField(choices=TIPO_DOCUMENTO_CHOICES, max_length=100)
    numero_documento = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField(default="2000-01-01")
    empresa_aportante = models.ForeignKey(Empresa_Aportante, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name



class Regimen(models.Model):
    tipo_regimen = models.CharField(choices=TIPO_REGIMEN_CHOICES, max_length=50)
    fuente_cotizacion = models.CharField(max_length=100)
    porcentaje_cotizacion = models.DecimalField(max_digits=5, decimal_places=2)
    def __str__(self):
        return self.tipo_regimen + " - " + self.fuente_cotizacion + " - " + str(self.porcentaje_cotizacion) + "%"
    




class Eps(models.Model):
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(choices=TIPO_EPS_CHOICES, max_length=50)
    nit = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nombre

class AdministradorEPS(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_documento = models.CharField(choices=TIPO_DOCUMENTO_CHOICES, max_length=100)
    numero_documento = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField(default="2000-01-01")
    eps = models.ForeignKey(Eps, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

class Departamento(models.Model):
    nombre = models.CharField(max_length=100)
    codigo_dane = models.CharField(max_length=10, unique=True)
    

    def __str__(self):
        return self.nombre   
class Municipio (models.Model):
    nombre = models.CharField(max_length=100)
    codigo_dane = models.CharField(max_length=10, unique=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre
class SedeEPS(models.Model):
    eps = models.ForeignKey(Eps, on_delete=models.CASCADE)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=300)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    horario_atencion = models.CharField(max_length=100)

    def __str__(self):
        return f"Sede de {self.eps.nombre} - {self.direccion}"

