# Generated by Django 2.2.6 on 2020-05-14 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sramais', '0012_auto_20200513_0833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ramais',
            name='Função',
            field=models.CharField(choices=[('Estagiário (a)', 'Estagiário (a)'), ('Funcionário (a)', 'Funcionário (a)'), ('Temporário (a)', 'Temporário (a)'), ('Terceirizado (a)', 'Terceirizado (a)')], max_length=25, null=True, verbose_name='Função'),
        ),
        migrations.RemoveField(
            model_name='ramais',
            name='unidade',
        ),
        migrations.AddField(
            model_name='ramais',
            name='unidade',
            field=models.ManyToManyField(null=True, to='Sramais.Unidade'),
        ),
        migrations.AlterField(
            model_name='unidade',
            name='descrição',
            field=models.TextField(unique=True),
        ),
        migrations.AlterField(
            model_name='unidade',
            name='nome_completo',
            field=models.CharField(max_length=70, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='unidade',
            name='sigla',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
