from django.contrib import admin

from .models import Profile, Sedes

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


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Sedes, SedesAdmin)