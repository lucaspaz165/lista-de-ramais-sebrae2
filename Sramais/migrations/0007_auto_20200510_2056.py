# Generated by Django 2.2.6 on 2020-05-11 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sramais', '0006_delete_favorito'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ramais',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=100, unique=True),
        ),
    ]