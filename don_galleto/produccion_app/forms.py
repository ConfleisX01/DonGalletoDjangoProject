# forms.py en produccion_app
from django import forms
from materia_prima.models import MateriaPrima
from Recetas_app.models import Receta
from produccion_app.models import LoteGalletas


class CrearProductoRegistrarForm(forms.ModelForm):
    class Meta:
        model = LoteGalletas
        fields = ['galleta', 'cantidad', 'fecha_produccion', 'fecha_caducidad']
        widgets = {
            'galleta': forms.Select(attrs={"class": "form-select"}),
            'cantidad': forms.NumberInput(attrs={"class": "form-control", "type": "number"}),
            'fecha_produccion': forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            'fecha_caducidad': forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }

class EditarProductoForm(forms.ModelForm):
    class Meta:
        model = LoteGalletas
        fields = ['galleta', 'cantidad', 'fecha_produccion', 'fecha_caducidad']
        widgets = {
            'galleta': forms.Select(attrs={"class": "form-select"}),
            'cantidad': forms.NumberInput(attrs={"class": "form-control", "type": "number"}),
            'fecha_produccion': forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            'fecha_caducidad': forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }
        def save(self):
            insumo = self.instance 
            insumo.galleta = self.cleaned_data['galleta']
            insumo.cantidad = self.cleaned_data['cantidad']
            insumo.fecha_produccion = self.cleaned_data['fecha_produccion']
            insumo.fecha_caducidad = self.cleaned_data['fecha_caducidad']
            insumo.save()


class CrearSolicitudProduccionForm(forms.ModelForm):
    class Meta:
        model = LoteGalletas
        fields = ['galleta',]
        widgets = {
            'usuario': forms.Select(attrs={"class": "form-select"}),
            'galleta': forms.Select(attrs={"class": "form-select"}),
            'fecha_solicitud': forms.DateInput(attrs={"class": "form-control", "type": "date"}),      
        }
    def save(self):
        insumo = self.instance 
        insumo.galleta = self.cleaned_data['galleta']
        insumo.usuario = self.cleaned_data['usuario']
        insumo.fecha_solicitud = self.cleaned_data['fecha_solicitud']
        insumo.save()