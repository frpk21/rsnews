# Generated by Django 2.2.1 on 2022-07-22 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('noticias', '0007_auto_20220722_1157'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publicados',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activo', models.BooleanField(default=True, null=True)),
                ('creado', models.DateTimeField(auto_now_add=True, null=True)),
                ('modificado', models.DateTimeField(auto_now=True, null=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='noticias.Noticias')),
                ('sede', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='noticias.Sedes')),
            ],
            options={
                'verbose_name_plural': 'Publicados',
            },
        ),
    ]