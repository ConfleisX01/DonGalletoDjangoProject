from django.contrib.auth.models import User
from django import forms


# Formulario para crear usuarios
class crearUsuariosForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), min_length=8, label='Contraseña')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'username': 'Nombre de usuario',
            'email': 'Correo electronico',
            'password': 'Contraseña',
        }
        help_texts = {
            'first_name': 'Nombre del usuario',
            'last_name': 'Apellido del usuario',
            'username': 'Nombre de usuario',
            'email': 'Correo electronico',
            'password': 'Contraseña',
        }
        error_messages = {
            'username': {
                'max_length': 'El nombre de usuario es muy largo',
                'required': 'El nombre de usuario es requerido',
            },
            'email': {
                'max_length': 'El correo electronico es muy largo',
                'required': 'El correo electronico es requerido',
            },
            'password': {
                'min_length': 'La contraseña es muy corta, son necesarios al menos 8 caracteres',
                'required': 'La contraseña es requerida',
            },
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

