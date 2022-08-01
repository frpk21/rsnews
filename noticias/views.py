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
from .models import Categorias_fotos, Noticias, Sedes, Fotos
from .forms import NoticiasForm, FotosForm, BuscarFotosForm
from catalogos.models import Categoria, SubCategoria
from noticias.forms import SuscribirseForm


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('obj1', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def InsertPostSonajero(sitio, post):
    with connections['sonajero'].cursor() as cursor:
        cursor.execute("INSERT INTO  generales_noticias (\
            modificado, \
            subcategoria, \
            titulo, \
            subtitulo, \
            descripcion, \
            archivo_audio, \
            urlvideo, \
            fecha_inicio_publicacion, \
            fecha_final_publicacion, \
            orden_destacado, \
            imagen_destacado, \
            autor, \
            fuente, \
            html, \
            pdf, \
            slug \
            ) VALUES (YEAR(NOW()),\
             )")
        v_bog1 = namedtuplefetchall(cursor)

class NoticiasListView(LoginRequiredMixin, generic.ListView):
    login_url = 'generales:login'
    model = Noticias
    template_name = "noticias/noticias_list.html"

    def get(self, request, *args, **kwargs):
        #filter(estado=0)
        noticias = Noticias.objects.all().order_by('-id')
        self.object_list = noticias
        context = super(NoticiasListView, self).get_context_data(*args, **kwargs)
        return self.render_to_response(
            self.get_context_data(
                obj = noticias,
                grupo=request.user.groups.get(user=request.user),
                sede = self.request.user.profile.sede.nombre_sede
            )
        )

def FotosListView(request):
    template_name = 'noticias/photos.html'
    hoy = date.today()
    context = {'hoy': hoy,
        'tags': '',
        'categoria': Categorias_fotos.objects.all().order_by('nombre')
        }
 
    if request.POST.get('buscar'):
        buscar = (request.POST.get('buscar').upper())
        template_name="generales/search.html"
        try:
            resultado = Fotos.objects.filter(tags__icontains=buscar).order_by('-id')
        except:
            resultado = Fotos.objects.filter(tags__icontains=buscar).order_by('-id')
        context['form_search'] = resultado
    else:
        buscar = ''
        resultado={}

    context['resultado'] = resultado

    return render(request, template_name, context)

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
            'inrai_video': '',
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
            'inrai_video': item.inrai_video,
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
        context['categorias'] = Categoria.objects.filter(activo=True).order_by('nombre')
        context['subcategorias'] = SubCategoria.objects.filter(activo=True).order_by('categoria__nombre','nombre')

        return context


class NoticiasCategoriaView(LoginRequiredMixin, generic.TemplateView):
    permission_required='noticias.view_noticias'
    model=Noticias
    template_name="noticias/noticia_cat.html"
    context_object_name="post" 
    def get_context_data(self, **kwargs):
        hoy = date.today()
        mes_actual = hoy.month
        ano_actual = hoy.year
        context = super().get_context_data(**kwargs)
        grupo=self.request.user.groups.get(user=self.request.user)
        sede=self.request.user.profile.sede
        context['grupo'] = grupo
        context['sede'] = sede
        context['cat_name'] = Categoria.objects.get(id=kwargs["pk"])
        context['post_cat'] = Noticias.objects.filter(subcategoria__categoria=kwargs["pk"]).order_by('-id')
        context['post_hoy'] = Noticias.objects.filter(modificado__date=hoy).exclude(subcategoria__categoria=kwargs["pk"])
        context['categorias'] = Categoria.objects.filter(activo=True).order_by('nombre')
        context['subcategorias'] = SubCategoria.objects.filter(activo=True).order_by('categoria__nombre','nombre')

        return context

def AprobarPostAjax(request, *args, **kwargs):
    pk = int(request.GET.get('pk', 0))
    estado_r = int(request.GET.get('estado', 0))
    if pk == "NaN" or pk < 1:
        return JsonResponse(data={'res': '', 'errors': 'No se pudo actulizar.'})
    else:
        Noticias.objects.filter(id=pk).update(estado=estado_r)
        return JsonResponse(data={"res": 'Hecho', 'errors': ''}, safe=False)
