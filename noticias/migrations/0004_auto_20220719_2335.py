# Generated by Django 2.2.1 on 2022-07-20 04:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('noticias', '0003_suscribir'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='noticias',
            name='autor',
        ),
        migrations.RemoveField(
            model_name='noticias',
            name='publicar_en',
        ),
        migrations.RemoveField(
            model_name='noticias',
            name='subcategoria',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='sede',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Suscribir',
        ),
        migrations.DeleteModel(
            name='Noticias',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
        migrations.DeleteModel(
            name='Sedes',
        ),
    ]