from django import forms
from materia_prima.models import MateriaPrima

class CrearMateriaPrimaForm(forms.ModelForm):
    class Meta:
        model = MateriaPrima
        fields = ['nombre_insumo', 'unidad_base']
        widgets = {
            'nombre_insumo': forms.TextInput(attrs={"class": "form-control", "type": "text"}),
            'unidad_base': forms.Select(attrs={"class": "form-select"})  # Esto es para el campo de unidades
        }

class EditarMateriaPrimaForm(forms.ModelForm):
    class Meta:
        model = MateriaPrima
        fields = ['nombre_insumo', 'unidad_base']
        widgets = {
            'nombre_insumo': forms.TextInput(attrs={"class": "form-control", "type": "text"}),
            'unidad_base': forms.Select(attrs={"class": "form-select"})  # Esto es para el campo de unidades
        }

    def save(self):
        insumo = self.instance
        insumo.nombre_insumo = self.cleaned_data['nombre_insumo']
        insumo.unidad_base = self.cleaned_data['unidad_base']
        insumo.save()