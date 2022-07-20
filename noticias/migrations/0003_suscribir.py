# Generated by Django 2.2.1 on 2022-07-19 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('noticias', '0002_noticias'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suscribir',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activo', models.BooleanField(default=True, null=True)),
                ('creado', models.DateField(auto_now_add=True, null=True)),
                ('modificado', models.DateField(auto_now=True, null=True)),
                ('email', models.CharField(help_text='eMail', max_length=200, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Suscribirse',
            },
        ),
    ]
