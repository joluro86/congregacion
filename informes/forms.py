from django.forms import ModelForm
from informes.models import InformeMensual

class InfomeMensualForm(ModelForm):
    class Meta:
        model = InformeMensual
        fields = ['mes', 'año', 'estado']
        
        def __init__(self, *args, **kwargs):
            super(InfomeMensualForm, self).__init__(*args, **kwargs)
            self.fields['mes'].widget.attrs['class'] = 'form-control'
            self.fields['año'].widget.attrs['class'] = 'form-control'
            self.fields['estado'].widget.attrs['class'] = 'form-control'


        
