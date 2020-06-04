from django import forms
from django.forms import ClearableFileInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Ramais, Unidade, Favorito
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class RamaisForm(forms.ModelForm):  # FORMULARIO RAMAIS
    
    class Meta:
        model = Ramais
        exclude = ['user']
        fields = '__all__'
        widgets = {'whatsapp': forms.TextInput(attrs={'data-mask': "00 - 0000-00000"}),
                   'admin': forms.HiddenInput()}


class UnidadeForm(forms.ModelForm):     # FORMULARIO UNIDADE
    class Meta:
        model = Unidade
        fields = '__all__'


class FavoritoForm(forms.ModelForm):
    class Meta:
        model = Favorito
        exclude = ['user']
        fields = '__all__'


class RegistroForm(UserCreationForm):    # FORMULARIO REGISTRO DE USUARIO
    email = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ['username', 'email'

                  ]
        labels = {'Usuário': 'username', 'Email': 'email'
                  }
