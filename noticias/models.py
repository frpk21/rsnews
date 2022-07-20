from django.db import models
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField
import os
from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
#from multiselectfield import MultiSelectField
from generales.models import ClaseModelo
from catalogos.models import SubCategoria
 
class Sedes(ClaseModelo):
    sede = models.IntegerField(default=0, null=False, blank=False)
    nombre_sede = models.CharField(blank=False, null=False, max_length=100, default="")

    def __str__(self):
        return '{}-{}'.format(self.id, self.nombre_sede)

    def save(self):
        self.nombre_sede = self.nombre_sede.upper()
        super(Sedes, self).save()

    class Meta:
        verbose_name_plural = "Sedes"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto = models.FileField("Archivo con Foto del Usuario", upload_to="fotos/", blank=False, null=False, default="")
    sede = models.ForeignKey(Sedes, on_delete=models.CASCADE, default=0, null=False, blank=False)
 
    def save(self):
        super(Profile, self).save()


class Noticias(ClaseModelo):
    subcategoria=models.ForeignKey(SubCategoria, on_delete=models.CASCADE, default=0, null=False, blank=False)
    titulo = models.CharField(help_text='Título de la noticia', blank=False, null=False, max_length=200)
    subtitulo = models.CharField(help_text='Sub título de la noticia', blank=False, null=False, max_length=500)
    descripcion = RichTextField(max_length=15000, blank=True, null=True)
    archivo_audio = models.FileField("Archivo Audio", upload_to="audio/", blank=True, null=True, default='')
    urlvideo = models.CharField('URL Youtube', blank=True, null=True, default='', max_length=200)
    vimeo_id = models.CharField(max_length=200,default=None, blank=True, null=True)
    viral = models.BooleanField(default=False)
    ultima_hora = models.BooleanField()
    fecha_inicio_publicacion = models.DateField('Fecha de inicio de publicación', blank=True, null=True, default=datetime.now)
    fecha_final_publicacion = models.DateField('Fecha de finalización de publicación', blank=True, null=True, default=datetime.now)
    CHOICES = ((0,'Principal'),(1,'Destacado 1'),(2,'Destacado 2'),(3,'Destacado 3'),(4,'General 4'))
    orden_destacado = models.IntegerField(choices=CHOICES, default=0, blank=False, null=False)
    imagen_destacado = models.FileField("Imagen Destacado", upload_to="imagenes/", blank=True, null=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,default='')
    fuente = models.CharField(help_text='Fuente noticia', blank=False, null=False, max_length=50, default="INRAI")
    html = models.TextField(max_length=10000, default="", blank=True, null=True)
    pdf = models.FileField("Archivo PDF", upload_to="pdf/", blank=True, null=True, default='')
    slug = models.SlugField(blank=True,null=True, max_length=250)
    CHOICES1 = ((0,'En aprobación'),(1,'Devuelto para revisión'),(2,'Rechazado'),(3,'Aprobado'),(4,'Publicado'))
    estado = models.IntegerField(choices=CHOICES1, default=0, blank=False, null=False)
    publicar_en = models.ManyToManyField(Sedes, related_name='Destinos_publicadas') 

    def __str__(self):
        return '{}-{}'.format(self.titulo, self.usuario.profile.sede.nombre_sede)

    def save(self):
        self.slug = slugify(self.titulo)
        super(Noticias, self).save()

    class Meta:
        verbose_name_plural = "Noticias"




class Suscribir(ClaseModelo):
    email = models.CharField(max_length=200, help_text='eMail', unique=True)

    def __str__(self):
        return '{}'.format(self.email)

    class Meta:
        verbose_name_plural = "Suscribirse"