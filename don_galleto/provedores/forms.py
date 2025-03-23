from django import forms
from provedores.models import Provedor

class ProvedorRegistrarForm(forms.ModelForm):
    provedor_nombre = forms.CharField(
        max_length=150,
        label="Nombre",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el Nombre'})
    )
    
    provedor_telefono = forms.CharField(
        max_length=15,
        label="Telefono",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el Telefono'})
    )
    
    provedor_identificacionNumero = forms.CharField(
        max_length=30,
        label="Numero de Identificacion",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el Numero de Identificación'})
    )
    
    provedor_razonSocial = forms.CharField(
        max_length=15,
        label="Razon Social",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese La razon social'})
    )
    
    provedor_direccion = forms.CharField(
        max_length=150,
        label="Direccion",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la Dirección'})
    )
    
    provedor_email = forms.CharField(
        max_length=50,
        label="Email",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el correo electronico'})
    )
    
    provedor_tipo = forms.CharField(
        max_length=50,
        label="Tipo",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el Tipo de producto'})
    )

    class Meta:
        model = Provedor
        fields = ['provedor_nombre', 'provedor_telefono', 'provedor_identificacionNumero', 'provedor_razonSocial', 'provedor_direccion', 'provedor_email', 'provedor_tipo']
    def save(self):
        item = Provedor(
            provedor_nombre=self.cleaned_data["provedor_nombre"],
            provedor_telefono=self.cleaned_data["provedor_telefono"],
            provedor_identificacionNumero=self.cleaned_data["provedor_identificacionNumero"],
            provedor_razonSocial=self.cleaned_data["provedor_razonSocial"],
            provedor_direccion=self.cleaned_data["provedor_direccion"],
            provedor_email=self.cleaned_data["provedor_email"],
            provedor_tipo=self.cleaned_data["provedor_tipo"]
        )
        item.save()

class ProvedorEditarForm(forms.ModelForm):
    provedor_nombre = forms.CharField(
        max_length=150,
        label="Nombre",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el Nombre'})
    )
    
    provedor_telefono = forms.CharField(
        max_length=15,
        label="Telefono",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el Telefono'})
    )
    
    provedor_identificacionNumero = forms.CharField(
        max_length=30,
        label="Numero_Identificacion",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el Numero de Identificación'})
    )
    
    provedor_razonSocial = forms.CharField(
        max_length=15,
        label="Razon_Social",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese La razon social'})
    )
    
    provedor_direccion = forms.CharField(
        max_length=150,
        label="Direccion",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la Dirección'})
    )
    
    provedor_email = forms.CharField(
        max_length=50,
        label="Email",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el correo electronico'})
    )
    
    provedor_tipo = forms.CharField(
        max_length=50,
        label="Tipo",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el Tipo de producto'})
    )
    
    estatus = forms.BooleanField(
        initial = False,
        label = 'estatus',
        required = False
    )
    
    class Meta:
        model = Provedor
        fields = ['provedor_nombre', 'provedor_telefono', 'provedor_identificacionNumero', 'provedor_razonSocial', 'provedor_direccion', 'provedor_email', 'provedor_tipo','estatus']
    def save(self, id):
        item = Provedor.objects.filter(id=id).first()
        item.provedor_nombre = self.cleaned_data["provedor_nombre"]
        item.provedor_telefono = self.cleaned_data["provedor_telefono"]
        item.provedor_identificacionNumero = self.cleaned_data["provedor_identificacionNumero"]
        item.provedor_razonSocial = self.cleaned_data["provedor_razonSocial"]
        item.provedor_direccion = self.cleaned_data["provedor_direccion"]
        item.provedor_email = self.cleaned_data["provedor_email"]
        item.provedor_tipo = self.cleaned_data["provedor_tipo"]
        item.estatus = self.cleaned_data["estatus"]
        item.save()