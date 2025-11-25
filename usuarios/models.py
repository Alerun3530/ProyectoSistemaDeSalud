from django.db import models
from django.contrib.auth.models import User

# Create your models here.
TIPO_DOCUMENTO_CHOICES = [
    ('CC', 'Cedula de Ciudadania'), 
    ('TI', 'Tarjeta de Identidad'), 
    ('CE', 'Cedula de Extranjeria'), 
    ('PP', 'Pasaporte')]


    

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_documento = models.CharField(choices=TIPO_DOCUMENTO_CHOICES, max_length=100)
    numero_documento = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField(default="2000-01-01")

    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name



class Documento(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100)
    archivo = models.FileField(upload_to='documentos/')
    
    
    
    def __str__(self):
        return self.usuario.user.first_name + " " + self.usuario.user.last_name
    
class Sisben(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    clasificacion = models.CharField(max_length=10)
    fecha_actualizacion = models.DateField(auto_now=True)

    def __str__(self):
        return f"Sisben de {self.usuario.user.first_name} - Puntaje: {self.clasificacion}"

class Beneficiario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    beneficiario = models.ForeignKey(Usuario, related_name='beneficiarios', on_delete=models.CASCADE)
    parentesco = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(default="2000-01-01")


    def __str__(self):
        return f"{self.beneficiario.user.first_name} ({self.parentesco}) - {self.usuario.user.username}"

