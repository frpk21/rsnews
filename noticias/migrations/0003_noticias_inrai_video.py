# Generated by Django 2.2.1 on 2022-07-27 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('noticias', '0002_remove_noticias_video_destacado'),
    ]

    operations = [
        migrations.AddField(
            model_name='noticias',
            name='inrai_video',
            field=models.TextField(blank=True, default='', max_length=10000, null=True, verbose_name='Video Streaming Inrai'),
        ),
    ]
