from django import forms

from catalogos.models import Categoria, SubCategoria

from django.forms.models import inlineformset_factory


class CategoriaForm(forms.ModelForm):
    class Meta:
        model=Categoria
        fields = ['nombre', 'activo'] 
        labels = {'nombre': "Descripción de la Catagoría",
                  'activo': "Estado"}
        widget = {'nombre': forms.TextInput()}

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })




class SubCategoriaForm(forms.ModelForm):
    categoria=forms.ModelChoiceField(
        queryset=Categoria.objects.filter(activo=True).
        order_by('nombre')
    )
    class Meta:
        model=SubCategoria
        fields = ['categoria','nombre', 'activo'] 
        labels = {'categoria': "Categoría",
                  'nombre': "Descripción de la Catagoría",
                  'activo': "Estado"}
        widget = {'nombre': forms.TextInput()}

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['categoria'].empty_label="Seleccione un categería:"
