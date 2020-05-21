from django.contrib import admin
from .models import Ramais, Unidade, Favorito


class RamaisAdmin(admin.ModelAdmin):
    list_display = ('nome', 'user', 'unidade', 'ramal')


admin.site.register(Ramais, RamaisAdmin)
admin.site.register(Unidade)
admin.site.register(Favorito)



