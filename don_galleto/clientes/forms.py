from django.contrib.auth.models import User
from django import forms
from clientes.models import Cliente

class ClienteCrearForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )

    class Meta:
        model = Cliente
        fields = []

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )

        cliente = Cliente.objects.create(user=user, user_type='cliente')

        return cliente

class ClienteEditarForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Cliente
        fields = ['username', 'email', 'password']

    def save(self):
        user = self.instance.user
        user.username = self.cleaned_data['username']
        user.email  = self.cleaned_data['email']
        user.password = self.cleaned_data['password']
        user.save()