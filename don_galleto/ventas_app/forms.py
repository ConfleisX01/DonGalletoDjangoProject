from django import forms
from ventas_app.models import VentaDetalle
from Recetas_app.models import Receta

class DetallesProductoForm(forms.ModelForm):
    cantidad = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad total a comprar'})
    )

    fecha_recoleccion = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    receta = forms.ModelChoiceField(
        queryset=Receta.objects.all(),
        widget=forms.HiddenInput()  # Ocultamos el campo en la interfaz
    )

    class Meta:
        model = VentaDetalle
        fields = ['cantidad', 'tipo_unidad', 'fecha_recoleccion', 'receta']
        widgets = {
            'tipo_unidad': forms.Select(attrs={"class": "form-select"})
        }