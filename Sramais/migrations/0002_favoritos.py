# Generated by Django 2.2.6 on 2020-05-05 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sramais', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favoritos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ramais', models.ForeignKey(blank=True, null=True, on_delete='CASCADE', to='Sramais.Ramais')),
            ],
        ),
    ]
