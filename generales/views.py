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
from generales.forms import MesAnoForm


class SinPrivilegios(PermissionRequiredMixin):
    login_url='generales:sin_privilegios'
    raise_exception=False
    redirect_field_name="redirecto_to"

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy(self.login_url))


class HomePage(generic.View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Pagina de Inicio')

class Home(LoginRequiredMixin, generic.TemplateView):
    template_name='generales/home.html'
    login_url='generales:login'

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

