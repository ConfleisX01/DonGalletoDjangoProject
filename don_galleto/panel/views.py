from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from usuarios_app.models import Usuario
from django.urls import reverse_lazy

@login_required
@permission_required('panel.view_panel', raise_exception=True)
def panelIndex(request):
    # Verificar si el usuario tiene un perfil asociado
    if not hasattr(request.user, 'usuario'):
        # Si no tiene perfil, crearlo
        Usuario.objects.create(user=request.user, telefono='', user_type='usuario')

    # Ahora que estamos seguros de que el usuario tiene un perfil
    user_type = request.user.usuario.user_type

    if user_type != 'admin':
        return render(request, 'error.html', {'message': 'Solo los administradores pueden acceder al panel de control'})
    
    return render(request, 'panel')

