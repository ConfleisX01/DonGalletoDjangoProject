from django import forms
from ventas_app.models import VentaDetalle, Venta
from Recetas_app.models import Receta
from django.forms import inlineformset_factory

class DetallesProductoForm(forms.ModelForm):
    cantidad = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad total a comprar'})
    )

    receta = forms.ModelChoiceField(
        queryset=Receta.objects.all(),
        widget=forms.HiddenInput()  # Ocultamos el campo en la interfaz
    )

    class Meta:
        model = VentaDetalle
        fields = ['cantidad', 'tipo_unidad', 'receta']
        widgets = {
            'tipo_unidad': forms.Select(attrs={"class": "form-select"})
        }
        
        

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = []  # La venta se genera automáticamente

class VentaDetalleForm(forms.ModelForm):
    class Meta:
        model = VentaDetalle
        fields = ["receta", "cantidad"]  # receta es para saber la galleta vendida y la cantidad

    receta = forms.ModelChoiceField(
        queryset=Receta.objects.all(),
        label="Galleta",
        empty_label="Seleccione una galleta...",  # ✅ Texto para la opción nula
        required=False,  # ✅ Permite enviar el formulario sin selección
    )
    cantidad = forms.IntegerField(min_value=1, label="Cantidad")

# Crear un Formset para manejar múltiples productos
VentaDetalleFormSet = inlineformset_factory(
    Venta,  # Modelo principal
    VentaDetalle,  # Modelo dependiente
    form=VentaDetalleForm,
    extra=0,  # Número de formularios en blanco
    can_delete=True  # Permitir eliminar productos en la venta
)