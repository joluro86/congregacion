from django.forms import ModelForm
from admin_congregacion.models import Publicador
from django import forms

class PublicadorForm(ModelForm):
    class Meta:
        model = Publicador
        fields = ['nombre', 'grupo', 'tipo', 'sexo', 'precursor', 'estado']

        nombre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))