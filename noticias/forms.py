from django import forms

from catalogos.models import Categoria, SubCategoria

from django.forms.models import inlineformset_factory

from noticias.models import Suscribir


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