from django import forms
from django.forms.models import inlineformset_factory
from datetime import date


hoy = date.today()
mes_actual = hoy.month
CHOICES = [
    (1,'ENERO'),
    (2,'FEBRERO'),
    (3,'MARZO'),
    (4,'ABRIL'),
    (5,'MAYO'),
    (6,'JUNIO'),
    (7,'JULIO'),
    (8,'AGOSTO'),
    (9,'SEPTIEMBRE'),
    (10,'OCTUBRE'),
    (11,'NOVIEMBRE'),
    (12,'DICIEMBRE')
    ]

class MesAnoForm(forms.Form):
    mes_consulta = forms.DateField(widget=forms.SelectDateWidget(months=CHOICES))


