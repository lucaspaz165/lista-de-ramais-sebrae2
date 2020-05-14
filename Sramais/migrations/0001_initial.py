# Generated by Django 2.2.6 on 2020-05-04 16:27

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Unidade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_completo', models.CharField(max_length=70, null=True)),
                ('sigla', models.CharField(max_length=10)),
                ('descrição', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Ramais',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, null=True)),
                ('ramal', models.DecimalField(decimal_places=0, max_digits=4)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(default='', max_length=100, unique=True)),
                ('whatsapp', models.CharField(max_length=15, null=True, verbose_name='whatsapp')),
                ('dia_de_nascimento', models.DecimalField(decimal_places=0, max_digits=2, null=True, validators=[django.core.validators.MaxValueValidator(31)], verbose_name='Dia de nascimento')),
                ('mes_de_nascimento', models.DecimalField(decimal_places=0, max_digits=2, null=True, validators=[django.core.validators.MaxValueValidator(12)], verbose_name='Mês de nascimento')),
                ('foto', models.ImageField(blank=True, null=True, upload_to='%Y/%m/%d/')),
                ('Função', models.CharField(choices=[('ESTAGIÁRIO(A)', 'ESTAGIÁRIO(A)'), ('FUNCIONÁRIO(A)', 'FUNCIONÁRIO(A)'), ('TEMPORÁRIO(A)', 'TEMPORÁRIO(A)'), ('TERCEIRIZADO(A)', 'TERCEIRIZADO(A)')], max_length=25, null=True, verbose_name='Função')),
                ('admin', models.BooleanField(blank=True, max_length=10, null=True)),
                ('unidade', models.ForeignKey(blank=True, null=True, on_delete='CASCADE', to='Sramais.Unidade')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]