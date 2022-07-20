from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from rsnews import settings
import datetime
import calendar
from datetime import date
from django.shortcuts import redirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.views.generic.list import ListView
from django.shortcuts import render
from django.db import connections
from collections import namedtuple
from django.http import JsonResponse
from datetime import datetime, timedelta
from generales.forms import MesAnoForm
from .models import Noticias
from catalogos.models import Categoria, SubCategoria
from noticias.forms import SuscribirseForm

def CategoriaView(request, pk):
    template_name = 'generales/seccion.html'

    hoy = date.today()
    id_titular=0
    titular = Noticias.objects.filter(subcategoria__categoria__id=pk).order_by('-id')[:1]
    for i, item in enumerate(titular):
        id_titular=item.id
        cat=item.subcategoria
    titulares1 = Noticias.objects.filter(orden_destacado=0, subcategoria__id=1).exclude(subcategoria=12).order_by('-id')[:2]
    #titular1 = Noticias.objects.filter(subcategoria__categoria__id=pk).exclude(id=id_titular).order_by('-id')[:1]
    #titular2 = Noticias.objects.filter(subcategoria__categoria__id=pk).exclude(id=id_titular).exclude(id=id_titular).order_by('-id')[:20]
    ultima_hora = Noticias.objects.filter(ultima_hora=True).order_by('-id')[:1]
    categorias = Categoria.objects.all().order_by("nombre")
    subcategorias = SubCategoria.objects.all().order_by("nombre")
    recientes = Noticias.objects.filter(viral=False, ultima_hora=False).exclude(subcategoria=12).order_by('-id')[:3]
    seccion = Categoria.objects.get(id=pk)
    noticias = Noticias.objects.filter(subcategoria__categoria__id=pk, ultima_hora=False).order_by('-id', 'subcategoria__id','orden_destacado')[:20]
    
    context = {'hoy': hoy, 'titular': titular, 'noticias': noticias, 'ultima_hora': ultima_hora, 'categorias': categorias,
               'subcategorias': subcategorias, 'seccion': seccion, 'cat': cat, 'titulares1': titulares1}
    context['regresivo'] = {'activo': False}
    if request.POST.get('buscar'):
        buscar = (request.POST.get('buscar').upper())
        template_name="generales/search.html"
        try:
            resultado = Noticias.objects.filter(titulo__icontains=buscar).order_by('-id')
            #paginator5 = Paginator(resultado, 10)
        except:
            resultado = Noticias.objects.filter(titulo__icontains=buscar).order_by('-id')
            #paginator5 = Paginator(resultado, 10)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        #try:
        #    resultado = paginator5.page(page)
        #except (EmptyPage, InvalidPage):
        #    resultado = paginator5.page(paginator5.num_pages)

        #context['paginator5'] = paginator5
    else:
        buscar = ''
        resultado={}
        
    context['resultado'] = resultado
    
    return render(request, template_name, context)
