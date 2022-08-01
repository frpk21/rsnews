from django.contrib import admin

from .models import Profile, Sedes, Categorias_fotos

from django.contrib.admin.widgets import AutocompleteSelect


class SedesAdmin(admin.ModelAdmin):
    list_display = ('nombre_sede', )
    ordering = ('nombre_sede', )

    class Meta:
        model = Sedes



class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'foto', 'sede',)
    ordering = ['user',]
    search_fields = ('user', )
    #autocomplete_fields = ['nit',]

    class Meta:
        model = Profile

class Categorias_fotosAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre', )

    class Meta:
        model = Categorias_fotos

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Sedes, SedesAdmin)
admin.site.register(Categorias_fotos, Categorias_fotosAdmin)