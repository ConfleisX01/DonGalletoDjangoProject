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
    cantidad = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad total a comprar'})
    )

    receta = forms.ModelChoiceField(
        queryset=Receta.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select', 'placeholder': 'Cantidad total a comprar'})
    )

    class Meta:
        model = VentaDetalle
        fields = ['receta', 'tipo_unidad', 'cantidad']
        widgets = {
            'tipo_unidad': forms.Select(attrs={"class": "form-select"}),
        }

class VentaDetalleForm(forms.ModelForm):
    class Meta:
        model = VentaDetalle
        fields = ["receta", "cantidad", "tipo_unidad"]  # Agregar unidad al form

    receta = forms.ModelChoiceField(
        queryset=Receta.objects.all(),
        label="Galleta",
        empty_label="Seleccione una galleta...",
        required=False,
    )
    cantidad = forms.IntegerField(min_value=1, label="Cantidad", required=True)

    tipo_unidad  = forms.ChoiceField(
        choices=[
            ('pq', 'Paq.'),  # Paquete (coincide con 'pq' de VentaDetalle)
            ('g', 'Gr.'),    # Gramos (cambiado de 'gr' a 'g' para coincidir)
            ('ud', 'Un.'),   # Unidad (igual que en VentaDetalle)
        ],
        label="Unidad",
        required=True,
        initial='ud',  # Establecer como 'Un.' por defecto
    )

    total = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0.0, widget=forms.HiddenInput())

    def clean(self):
        cleaned_data = super().clean()
        receta = cleaned_data.get('receta')
        cantidad = cleaned_data.get('cantidad')

        if receta and cantidad:
            total = receta.precio_galleta * cantidad
            cleaned_data['total'] = total
        return cleaned_data

# Crear un Formset para manejar múltiples productos
VentaDetalleFormSet = inlineformset_factory(
    Venta,  # Modelo principal
    VentaDetalle,  # Modelo dependiente
    form=VentaDetalleForm,
    extra=0,  # Número de formularios en blanco
    can_delete=True  # Permitir eliminar productos en la venta
)