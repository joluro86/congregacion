from django.forms import ModelForm
from informes.models import InformeMensual

class InfomeMensualForm(ModelForm):
    class Meta:
        model = InformeMensual
        fields = ['mes', 'año', 'estado']

