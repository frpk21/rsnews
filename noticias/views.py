from tkinter import FLAT
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
from .models import Noticias, Sedes
from .forms import NoticiasForm
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



class NoticiasListView(LoginRequiredMixin, generic.ListView):
    login_url = 'generales:login'
    model = Noticias
    template_name = "noticias/noticias_list.html"

    def get(self, request, *args, **kwargs):
        noticias = Noticias.objects.filter(estado=0).order_by('-id')
        self.object_list = noticias
        context = super(NoticiasListView, self).get_context_data(*args, **kwargs)
        return self.render_to_response(
            self.get_context_data(
                obj = noticias,
                grupo=request.user.groups.get(user=request.user),
                sede = self.request.user.profile.sede.nombre_sede
            )
        )


class NoticiaNew(LoginRequiredMixin, generic.CreateView):
    permission_required = 'noticias.add_noticias'
    model = Noticias
    login_url = 'generales:login'
    template_name = 'noticias/noticia_form.html'
    form_class = NoticiasForm
    success_url = reverse_lazy('noticias:noticia_list')

    def get(self, request, *args, **kwargs):
        sedes = Sedes.objects.all()
        ctx = {
            'subcategoria': '',
            'titulo': '',
            'subtitulo': '',
            'descripcion': '',
            'fecha_inicio_publicacion': datetime.today() + timedelta(days=(1)),
            'fecha_final_publicacion': datetime.today() + timedelta(days=(2)),
            'orden_destacado': 0,
            'imagen_destacado': '',
            'archivo_audio': '',
            'urlvideo': '',
            'viral': False,
            'ultima_hora': False,
            'fuente': '',
            'html': '',
            'pdf': ''
            }

        self.object = None
        form = NoticiasForm(initial=ctx)

        return self.render_to_response( 
            self.get_context_data(
                form=form,
                sedes=sedes,
                grupo=request.user.groups.get(user=request.user),
                sede=self.request.user.profile.sede
            )
        )

    def post(self, request, *args, **kwargs):
        form =NoticiasForm(request.POST, request.FILES)
        print("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
        print(form.errors)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.autor = self.request.user
        self.object = form.save()
        return HttpResponseRedirect(reverse_lazy("noticias:noticia_list"))

    def form_invalid(self, form):
        self.object=form
        return self.render_to_response(
            self.get_context_data(
                form=form,
                sede=self.request.user.profile.sede
            )
        )

class NoticiaEdit(LoginRequiredMixin, generic.UpdateView):
    permission_required='noticias.change_noticias'
    model=Noticias
    template_name="noticias/noticia_form.html"
    form_class=NoticiasForm
    success_url=reverse_lazy("noticias:noticia_list")

    def get(self, request, *args, **kwargs):
        post = Noticias.objects.filter(id=kwargs["pk"])
        for i, item in enumerate(post):
            ctx = {
            'subcategoria': item.subcategoria,
            'titulo': item.titulo,
            'subtitulo': item.subtitulo,
            'descripcion': item.descripcion,
            'fecha_inicio_publicacion': item.fecha_inicio_publicacion,
            'fecha_final_publicacion': item.fecha_final_publicacion,
            'orden_destacado': item.orden_destacado,
            'imagen_destacado': item.imagen_destacado,
            'archivo_audio': item.archivo_audio,
            'urlvideo': item.urlvideo,
            'viral': item.viral,
            'ultima_hora': item.ultima_hora,
            'fuente': item.fuente,
            'html': item.html,
            'pdf': item.pdf
            }
        self.object = None
        form = NoticiasForm(initial=ctx)

        return self.render_to_response( 
            self.get_context_data(
                form=form,
                grupo=request.user.groups.get(user=request.user),
                sede=self.request.user.profile.sede
            )
        )

    def post(self, request, *args, **kwargs):
        noticia = Noticias.objects.get(id=kwargs["pk"])
        form = NoticiasForm(request.POST, request.FILES, instance=noticia)

        if form.is_valid():
            post = form.save(commit=False)
            post.autor = self.request.user
            post.save()
            return HttpResponseRedirect(self.success_url)


class NoticiaView(LoginRequiredMixin, generic.TemplateView):
    permission_required='noticias.view_noticias'
    model=Noticias
    template_name="noticias/noticia_view.html"
    context_object_name="post" 
    def get_context_data(self, **kwargs):
        hoy = date.today()
        mes_actual = hoy.month
        ano_actual = hoy.year
        context = super().get_context_data(**kwargs)
        post = Noticias.objects.get(id=kwargs["pk"])
        grupo=self.request.user.groups.get(user=self.request.user)
        sede=self.request.user.profile.sede
        context['post'] = post
        context['grupo'] = grupo
        context['sede'] = sede
        context['post_hoy'] = Noticias.objects.filter(modificado__date=hoy).exclude(id=kwargs["pk"])
        context['categorias'] = SubCategoria.objects.filter(activo=True)

        return context