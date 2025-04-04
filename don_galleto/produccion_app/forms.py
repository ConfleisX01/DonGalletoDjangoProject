# forms.py en produccion_app
from django import forms
from materia_prima.models import MateriaPrima
from Recetas_app.models import Receta
from produccion_app.models import LoteGalletas, SolicitudProduccion


class SeleccionarReceta(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.nombre

class AgregarSolicitudForm(forms.ModelForm):
    galleta = forms.ModelChoiceField(
        queryset=Receta.objects.all(),
        label='Seleccionar galleta a solicitar',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = SolicitudProduccion
        fields = ['galleta']

    def save(self, commit=True):
        solicitud = super().save(commit=False)
        if commit:
            solicitud.save() 
        return solicitud