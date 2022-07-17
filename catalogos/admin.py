from django.contrib import admin
from .models import Categoria, SubCategoria
from django.contrib.admin.widgets import AutocompleteSelect


admin.site.register(Categoria)
admin.site.register(SubCategoria)
