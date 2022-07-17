from django.db import models

from generales.models import ClaseModelo

from django.contrib.auth.models import User

from datetime import datetime

# Create your models here.

class Categoria(ClaseModelo):
    nombre = models.CharField(
        max_length=100,
        help_text='Nombre de la categoría',
        unique=True,
    )

    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self):
        self.nombre = self.nombre.upper()
        super(Categoria, self).save()

    class Meta:
        verbose_name_plural = "Categorias"

 

class SubCategoria(ClaseModelo):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nombre = models.CharField(
        max_length=100,
        help_text='Descripción de la sub categoría'
    )

    def __str__(self):
        return '{}:{}'.format(self.categoria.nombre,self.nombre)

    def save(self):
        self.nombre = self.nombre.upper()
        super(SubCategoria, self).save()

    class Meta:
        verbose_name_plural = "Sub Categorias"
        unique_together = ('categoria','nombre')
