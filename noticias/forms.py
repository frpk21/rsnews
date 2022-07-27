from django import forms

from catalogos.models import Categoria, SubCategoria

from django.forms.models import inlineformset_factory

from noticias.models import Suscribir, Noticias, Publicados

from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker

from ckeditor.widgets import CKEditorWidget


class SuscribirseForm(forms.ModelForm):
    
    class Meta:
        model = Suscribir
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not email:
            raise forms.ValidationError("Email Requerido")
        return email


class NoticiasForm(forms.ModelForm):
    class Meta:
        model=Noticias
        fields = [
            'subcategoria',
            'titulo',
            'subtitulo',
            'descripcion',
            'fecha_inicio_publicacion',
            'fecha_final_publicacion',
            'orden_destacado',
            'imagen_destacado',
            'inrai_video',
            'archivo_audio',
            'urlvideo',
            'viral',
            'ultima_hora',
            'fuente',
            'html',
            'pdf',
        ]
    fecha_inicio_publicacion = forms.DateField(widget=DatePicker())
    fecha_final_publicacion = forms.DateField(widget=DatePicker())
    archivo_audio = forms.FileField()
    descripcion = forms.CharField(widget = CKEditorWidget())
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['fecha_inicio_publicacion'].widget.attrs.update({'style':'text-align: center;','type': 'datetime-local'})
        self.fields['fecha_final_publicacion'].widget.attrs.update({'style':'text-align: center;','type': 'datetime-local'})
        #self.fields['porc_descuento'].widget.attrs.update({'style':'text-align: center; color:red;'})
        #self.fields['valor_bruto'].widget.attrs.update({'onkeyup': 'format(this)', 'style':'text-align: right; color:red; font-size:14px; width: 200px;'})
        #self.fields['porc_descuento'].widget.attrs['readonly']= True
        #self.fields['valor_neto'].widget.attrs.update({'onkeyup': 'format(this)', 'style':'text-align: right; color:blue; font-size:14px; width: 200px;'})
        #self.fields['valor_neto'].widget.attrs.update({'onchange': 'valida_descuento(id)'})
        #self.fields['tcredito'].widget.attrs.update({'onkeyup': 'format(this)', 'style':'text-align: right; color:red; font-size:14px; width: 200px;'})
        #self.fields['transferencia'].widget.attrs.update({'onkeyup': 'format(this)', 'style':'text-align: right; color:red; font-size:14px; width: 200px;'})
        #self.fields['bonos'].widget.attrs.update({'onkeyup': 'format(this)', 'style':'text-align: right; color:red; font-size:14px; width: 200px;'})
        #self.fields['credito'].widget.attrs.update({'onkeyup': 'format(this)', 'style':'text-align: right; color:red; font-size:14px; width: 200px;'})
        #self.fields['descuento'].widget.attrs.update({'onkeyup': 'format(this)', 'style':'text-align: right; color:red; font-size:14px; width: 200px;'})
        self.fields['archivo_audio'].required = False


    def clean_subcategoria(self):
        subcategoria = self.cleaned_data["subcategoria"]
        if not subcategoria:
            raise forms.ValidationError("Subcategoria Requerida.")

        return subcategoria

    def clean_titulo(self):
        titulo = self.cleaned_data["titulo"]
        if not titulo:
            raise forms.ValidationError("Titulo Requerido.")

        return titulo

    def clean_subtitulo(self):
        subtitulo = self.cleaned_data["subtitulo"]
        if not subtitulo:
            raise forms.ValidationError("Sub titulo Requerido.")

        return subtitulo

    def clean_descripcion(self):
        descripcion = self.cleaned_data["descripcion"]
        if not descripcion:
            raise forms.ValidationError("Descripcion Requerido.")

        return descripcion

    def clean_fecha_inicio_publicacion(self):
        fecha_inicio_publicacion = self.cleaned_data["fecha_inicio_publicacion"]
        if not fecha_inicio_publicacion:
            raise forms.ValidationError("Fecha inicio de la publicacion requerida")
        return fecha_inicio_publicacion

    def clean_fecha_final_publicacion(self):
        fecha_final_publicacion = self.cleaned_data["fecha_final_publicacion"]
        if not fecha_final_publicacion:
            raise forms.ValidationError("Fecha final de la publicacion requerida")
        return fecha_final_publicacion

    def clean_archivo_audio(self):
        archivo_audio = self.cleaned_data["archivo_audio"]
        return archivo_audio

    def clean_urlvideo(self):
        urlvideo = self.cleaned_data["urlvideo"]
        return urlvideo

    def clean_viral(self):
        viral = self.cleaned_data["viral"]
        return viral

    def clean_ultima_hora(self):
        ultima_hora = self.cleaned_data["ultima_hora"]
        return ultima_hora
    
    def clean_orden_destacado(self):
        orden_destacado = self.cleaned_data["orden_destacado"]
        return orden_destacado

    def clean_fuente(self):
        fuente = self.cleaned_data["fuente"]
        return fuente

    def clean_html(self):
        html = self.cleaned_data["html"]
        return html

    def clean_pdf(self):
        pdf = self.cleaned_data["pdf"]
        return pdf
