from django.db import models

class Usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    id_rol = models.IntegerField(default=1)
    nombre = models.CharField(max_length=100)
    correo = models.CharField(unique=True, max_length=100)
    contrasena = models.CharField(max_length=255)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    saldo_metrocoins = models.IntegerField(blank=True, null=True, default=0)
    verificado = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        db_table = 'usuarios'

    def __str__(self) -> str:
        return self.nombre
