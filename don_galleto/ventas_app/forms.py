from django import forms
from ventas_app.models import Venta, VentaDetalle

class DetallesProductoForm(forms.ModelForm):
    total = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Precio total'})
    )

    cantidad = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad total a comprar'})
    )

    fecha_recoleccion = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    class Meta:
        model = VentaDetalle
        fields = ['total', 'cantidad', 'tipo_unidad', 'fecha_recoleccion', 'receta']
        widgets = {
            'tipo_unidad': forms.Select(attrs={"class": "form-select"})
        }