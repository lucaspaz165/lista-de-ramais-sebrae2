# Generated by Django 2.2.6 on 2020-05-18 23:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Sramais', '0003_favorito'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favorito',
            name='Favoritos',
        ),
        migrations.AddField(
            model_name='favorito',
            name='Favoritos',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Sramais.Ramais'),
        ),
    ]
