# Generated by Django 2.2.1 on 2022-07-18 22:50

import ckeditor.fields
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('noticias', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Noticias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activo', models.BooleanField(default=True, null=True)),
                ('creado', models.DateField(auto_now_add=True, null=True)),
                ('modificado', models.DateField(auto_now=True, null=True)),
                ('titulo', models.CharField(help_text='Título de la noticia', max_length=200)),
                ('subtitulo', models.CharField(help_text='Sub título de la noticia', max_length=500)),
                ('descripcion', ckeditor.fields.RichTextField(blank=True, max_length=15000, null=True)),
                ('archivo_audio', models.FileField(blank=True, default='', null=True, upload_to='audio/', verbose_name='Archivo Audio')),
                ('urlvideo', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='URL Youtube')),
                ('vimeo_id', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('viral', models.BooleanField(default=False)),
                ('ultima_hora', models.BooleanField()),
                ('fecha_inicio_publicacion', models.DateField(blank=True, default=datetime.datetime.now, null=True, verbose_name='Fecha de inicio de publicación')),
                ('fecha_final_publicacion', models.DateField(blank=True, default=datetime.datetime.now, null=True, verbose_name='Fecha de finalización de publicación')),
                ('orden_destacado', models.IntegerField(choices=[(0, 'Principal'), (1, 'Destacado 1'), (2, 'Destacado 2'), (3, 'Destacado 3'), (4, 'General 4')], default=0)),
                ('imagen_destacado', models.FileField(blank=True, null=True, upload_to='imagenes/', verbose_name='Imagen Destacado')),
                ('fuente', models.CharField(default='INRAI', help_text='Fuente noticia', max_length=50)),
                ('html', models.TextField(blank=True, default='', max_length=10000, null=True)),
                ('pdf', models.FileField(blank=True, default='', null=True, upload_to='pdf/', verbose_name='Archivo PDF')),
                ('slug', models.SlugField(blank=True, max_length=250, null=True)),
                ('estado', models.IntegerField(choices=[(0, 'En aprobación'), (1, 'Devuelto para revisión'), (2, 'Rechazado'), (3, 'Aprobado'), (4, 'Publicado')], default=0)),
                ('autor', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('publicar_en', models.ManyToManyField(related_name='Destinos_publicadas', to='noticias.Sedes')),
                ('subcategoria', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='catalogos.SubCategoria')),
            ],
            options={
                'verbose_name_plural': 'Noticias',
            },
        ),
    ]
