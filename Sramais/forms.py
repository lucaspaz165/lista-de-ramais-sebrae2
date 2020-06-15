from django import forms
from django.forms import ClearableFileInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Ramais, Unidade, Favorito
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class RamaisForm(forms.ModelForm):  # FORMULARIO RAMAIS
    nome = forms.CharField(required=True,
                           label='Nome',
                           widget=forms.TextInput(
                               attrs={'placeholder': 'Digite seu nome completo', 'style': 'height:' '3em;'},
                           ),
                           )
    ramal = forms.CharField(required=True,
                            label= 'Ramal',
                            widget=forms.TextInput(
                                attrs={'placeholder': 'Número de ramal', 'style': 'height:' '3em;'},
                            ),
                            )
    dia_de_nascimento = forms.CharField(required=True,
                            widget=forms.TextInput(
                                attrs={'placeholder': 'Digite seu dia de nascimento', 'style': 'height:' '3em;'},
                            ),
                            )
    mes_de_nascimento = forms.CharField(required=True,
                                        widget=forms.TextInput(
                                            attrs={'placeholder': 'Digite seu mes de nascimento',
                                                   'style': 'height:' '3em;'},
                                        ),
                                        )

    class Meta:
        model = Ramais
        exclude = ['user']
        fields = '__all__'
        widgets = {'whatsapp': forms.TextInput(attrs={'data-mask': "00 - 0000-00000", 'size': '80', 'style': 'height:'
                                                                                                             '3em;',
                                                      'placeholder': 'Digite o seu número de Whatsapp'}),
                   'admin': forms.HiddenInput(),
                   'unidade': forms.Select(attrs={'style': 'height:' '3em;', }),
                   'Função': forms.Select(attrs={'style': 'height:' '3em;', }),
        }


class UnidadeForm(forms.ModelForm):  # FORMULARIO UNIDADE
    nome_completo = forms.CharField(required=True,
                           label='Nome Completo da Unidade',
                           widget=forms.TextInput(
                               attrs={'placeholder': 'Digite o nome completo', 'style': 'height:' '3em;'},
                           ),
                           )
    sigla = forms.CharField(required=True,
                    label='Sigla',
                    widget=forms.TextInput(
                        attrs={'placeholder': 'Digite a sigla da unidade', 'style': 'height:' '3em;'},
                    ),
                    )
    descrição = forms.CharField(required=True,
                    label='Descrição',
                    widget=forms.TextInput(
                        attrs={'placeholder': 'Descreva as atividades da unidade', 'style': 'height:' '6em;'},
                    ),
                    )
    class Meta:
        model = Unidade
        fields = '__all__'


class FavoritoForm(forms.ModelForm):
    class Meta:
        model = Favorito
        exclude = ['user']
        fields = '__all__'


class RegistroForm(UserCreationForm):  # FORMULARIO REGISTRO DE USUARIO
    username = forms.CharField(required=True,
                           label='Usuário',
                           widget=forms.TextInput(
                               attrs={'placeholder': 'Digite seu nome de Usuário', 'style': 'height:' '3em;'},
                           ),
                           )
    email = forms.CharField(required=True,
                            max_length=100,
                            label='Email',
                            widget=forms.TextInput(
                                attrs={'placeholder': 'Digite seu email', 'style': 'height:' '3em;'},
                            ),
                            )

    password1 = forms.CharField(required=True,
                               label='Senha',
                               widget=forms.TextInput(
                                   attrs={'placeholder': 'Digite sua senha',
                                          'style': 'height:' '3em;', 'type': 'password'},
                               ),
                               )
    password2 = forms.CharField(required=True,
                                label='Confirmação da Senha',
                                widget=forms.TextInput(
                                    attrs={'placeholder': 'Confirme sua senha',
                                           'style': 'height:' '3em;', 'type': 'password'},
                                ),
                                )

    class Meta:

        model = User
        fields = ['username', 'email'

                  ]
        labels = {'Usuário': 'username', 'Email': 'email'
                  }
