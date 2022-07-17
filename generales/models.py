from django.db import models

class ClaseModelo(models.Model):
    activo = models.BooleanField(default=True, null=True)
    creado = models.DateField(auto_now_add=True, null=True)
    modificado = models.DateField(auto_now=True, null=True)

    class Meta:
        abstract=True
