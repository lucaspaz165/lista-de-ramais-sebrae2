# Generated by Django 2.2.6 on 2020-05-14 00:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Sramais', '0013_auto_20200513_1949'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ramais',
            name='unidade',
        ),
        migrations.AddField(
            model_name='ramais',
            name='unidade',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Sramais.Unidade'),
        ),
    ]