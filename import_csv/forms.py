from django import forms
from .models import Correspondencia  # Importa el modelo de correspondencia

class CorrespondenciaForm(forms.ModelForm):
    class Meta:
        model = Correspondencia  # Modelo asociado
        fields = '__all__'  # O especifica los campos que quieres usar, por ejemplo: ['campo1', 'campo2']
