# forms.py en produccion_app
from django import forms
from produccion_app.models import Produccion
from materia_prima.models import MateriaPrima
from Recetas_app.models import Receta

class CrearProduccionForm(forms.ModelForm):
    class Meta:
        model = Produccion
        fields = ['nombre_producto', 'cantidad_producida','cantidad_materia_prima_utilizada']
        widgets = {
            'nombre_producto': forms.Select(attrs={"class": "form-select"}), 
            'cantidad_producida': forms.NumberInput(attrs={"class": "form-control", "type": "number"}),
            'materia_prima': forms.Select(attrs={"class": "form-select"}),
            'cantidad_materia_prima_utilizada': forms.NumberInput(attrs={"class": "form-control", "type": "number"}),
        }

class EditarProduccionForm(forms.ModelForm):
    class Meta:
        model = Produccion
        fields = ['estado']
        widgets = {
            'estado': forms.Select(attrs={"class": "form-select"})
        }

    def save(self):
        produccion = self.instance
        produccion.estado = self.cleaned_data['estado']
        produccion.save()
