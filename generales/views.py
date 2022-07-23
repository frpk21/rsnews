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
from noticias.models import Noticias, Sedes
from catalogos.models import Categoria, SubCategoria
from noticias.forms import SuscribirseForm
from django.db.models import Count


class SinPrivilegios(PermissionRequiredMixin):
    login_url='generales:sin_privilegios'
    raise_exception=False
    redirect_field_name="redirecto_to"

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy(self.login_url))


class HomePage(generic.View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Pagina de Inicio')

#class Home(LoginRequiredMixin, generic.TemplateView):
#    template_name='generales/home.html'
#    login_url='generales:login'

def HomeView(request):
    template_name = 'generales/home.html'
    hoy = date.today()
    total_mes = Noticias.objects.filter(modificado__date__month=hoy.month).count()


    titulares1 = Noticias.objects.filter(orden_destacado=0, subcategoria__id=1).exclude(subcategoria=12).order_by('-id')[:2]
    titulares2 = Noticias.objects.filter(orden_destacado=0, subcategoria__id=2).order_by('-id')[:4]
    titulares3 = Noticias.objects.filter(orden_destacado=0, subcategoria__categoria__gte=2).exclude(subcategoria=12).order_by('-id')[:4]
    ultima_hora = Noticias.objects.filter(ultima_hora=True).order_by('-id')[:4]
    virales = Noticias.objects.filter(viral=True, ultima_hora=False, ).order_by('-id')[:5]
    deportes1 = Noticias.objects.filter(orden_destacado=1, ultima_hora=False, subcategoria__categoria=3).last()
    deportes2 = Noticias.objects.filter(orden_destacado=2, ultima_hora=False, subcategoria__categoria=3).last()
    deportes3 = Noticias.objects.filter(orden_destacado__gte=3, ultima_hora=False, subcategoria__categoria=3).last()
    deportes4 = Noticias.objects.filter(orden_destacado=4, ultima_hora=False, subcategoria__categoria=3).last()
    loquepasa = Noticias.objects.filter(viral=False, ultima_hora=False, subcategoria__categoria=1).exclude(fecha_inicio_publicacion__gte=hoy).order_by('-id')[:8]
    loquesuena = Noticias.objects.filter(viral=False, ultima_hora=False, subcategoria__categoria=2).exclude(fecha_inicio_publicacion__gte=hoy).order_by('-id')[:8]
    loquesemueve = Noticias.objects.filter(viral=False, ultima_hora=False, subcategoria__categoria=3).exclude(fecha_inicio_publicacion__gte=hoy).order_by('-id')[:8]
    sonajero = Noticias.objects.filter(viral=False, ultima_hora=False, subcategoria__categoria=4).order_by('-id')[:8]
    recientes = Noticias.objects.filter(viral=False, ultima_hora=False).exclude(subcategoria=12).order_by('-id')[:3]
    tecno1 = Noticias.objects.filter(viral=False, ultima_hora=False, orden_destacado=0, subcategoria=12).order_by('-id')[:2]
    tecno2 = Noticias.objects.filter(viral=False, ultima_hora=False, subcategoria=12).order_by('-id')[:4]
    lomasvisto = Noticias.objects.filter(ultima_hora=False).order_by('-vistas')[:4]
    populares = Noticias.objects.filter(viral=True, ultima_hora=False).order_by('-vistas')[:4]
    if not deportes3:
        deportes3 = Noticias.objects.filter(orden_destacado__gte=3, ultima_hora=False).last()
    if not ultima_hora:
        ultima_hora = Noticias.objects.all().order_by('-id')[:3]
    categorias = Categoria.objects.all().order_by("nombre")
    subcategorias = SubCategoria.objects.all().order_by("nombre")

    context = {'hoy': hoy,
        'tecno1': tecno1,
        'tecno2': tecno2,
        'lomasvisto': lomasvisto,
        'populares': populares,
        'recientes': recientes,
        'titulares1': titulares1,
        'sonajero': sonajero,
        'loquesuena': loquesuena,
        'loquesemueve': loquesemueve,
        'titulares2': titulares2,
        'titulares3': titulares3,
        'loquepasa': loquepasa,
        'ultima_hora': ultima_hora,
        'categorias': categorias,
        'subcategorias': subcategorias,
        'virales': virales,
        'deportes1': deportes1,
        'deportes2': deportes2,
        'deportes3': deportes3,
        'deportes4': deportes4
        }
    manana = hoy + timedelta(days=1)
    

    if request.POST.get('email'):
        form_home = SuscribirseForm(request.POST)
        if form_home.is_valid():
            post = form_home.save(commit=False)
            post.save()
            success_url=reverse_lazy("/")
            
            return JsonResponse(
                {
                    'content': {
                        'message': 'Gracias por suscribirse.',
                    }
                }
            )
        else:
            return JsonResponse(
                {
                    'content': {
                        'message': 'Ya ha sido registrado. Gracias!',
                    }
                }
            )
    else:
        form_home = SuscribirseForm()
        
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
        context['form_search'] = resultado
    else:
        buscar = ''
        resultado={}
        template_name = "generales/home.html"

    
    sede1=Sedes.objects.all().order_by('nombre_sede')
    sedes=[]
    for i, item in enumerate(sede1):
        val = Noticias.objects.filter(modificado__date__month=hoy.month, autor__profile__sede=item.id).count()
        sedes.append({'nombre':item.nombre_sede, 'valor':int(round(val * 100 / 220, 0))}) # 200 notas / mes como meta minima de produccion de contenido.

    #sedes=Sedes.objects.filter(id__gt=sede1.id).order_by('nombre_sede')
    context['form_home'] = form_home
    context['resultado'] = resultado
    context['total_mes'] = total_mes
    context['total_porc_mes'] = int(round(total_mes * 100 /1540, 0))  # 1540 noticias en total por mes
    context["tit"] = nombre_mes(hoy.month)+" DE "+str(hoy.year)
    context['sedes'] = sedes
    #context['sede1'] = sede1

    return render(request, template_name, context)


class HomeSinPrivilegios(generic.TemplateView):
    template_name="generales/msg_sin_privilegios.html"


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('obj1', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def nombre_mes(mesr):
    mesr=int(mesr)
    if mesr == 1:
        cmesr="ENERO"
    elif mesr == 2:
        cmesr="FEBRERO"
    elif mesr == 3:
        cmesr="MARZO"
    elif mesr == 4:
        cmesr="ABRIL"
    elif mesr == 5:
        cmesr="MAYO"
    elif mesr == 6:
        cmesr="JUNIO"
    elif mesr == 7:
        cmesr="JULIO"
    elif mesr == 8:
        cmesr="AGOSTO"
    elif mesr == 9:
        cmesr="SEPTIEMBRE"
    elif mesr == 10:
        cmesr="OCTUBRE"
    elif mesr == 11:
        cmesr="NOVIEMBRE"
    elif mesr == 12:
        cmesr="DICIEMBRE"

    return(cmesr)


def PoliticaView(request):
    hoy = date.today()
    anor = hoy.year
    
    return render(request, 'generales/privacy-policy.html')

