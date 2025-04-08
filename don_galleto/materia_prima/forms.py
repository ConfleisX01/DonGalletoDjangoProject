from django import forms
from materia_prima.models import MateriaPrima
from materia_prima.models import LoteMateriaPrima

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

class ComprarInsumoForm(forms.ModelForm):
    class Meta:
        model = LoteMateriaPrima
        fields = ['insumo', 'cantidad', 'fecha_caducidad', 'proveedor', 'costo_uniario']
        widgets = {
            'insumo': forms.Select(attrs={
                "class": "form-select",
                "placeholder": "Selecciona un insumo"
            }),
            'cantidad': forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Cantidad a comprar",
                "min": "0",
                "step": "0.01"
            }),
            'fecha_caducidad': forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            'proveedor': forms.Select(attrs={
                "class": "form-select",
                "placeholder": "Selecciona un proveedor"
            }),
            'costo_uniario': forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Costo unitario",
                "min": "0",
                "step": "0.01"
            })
        }

    def save(self):
        lote = self.instance
        lote.insumo = self.cleaned_data['insumo']
        lote.cantidad = self.cleaned_data['cantidad']
        lote.fecha_caducidad = self.cleaned_data['fecha_caducidad']
        lote.proveedor = self.cleaned_data['proveedor']
        lote.costo_uniario = self.cleaned_data['costo_uniario']
        lote.save()
        return lote