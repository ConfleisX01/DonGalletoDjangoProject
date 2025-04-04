from django.contrib import admin
from main.views import principal, panel, welcome
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main.views import registro 

from django.views.generic import TemplateView

from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('accounts/', include("django.contrib.auth.urls")),
    path('accounts/registro/', views.registro, name='registro'),
    path('panel/', panel, name='panel'),
    path('principal', principal, name='principal'),
    path('welcome', welcome, name='welcome'),
    path('usuarios/', include('usuarios_app.urls')),
    path('panel/', include('panel.urls')),
    path('provedores/', include('provedores.urls')),
    path('ventas/', include('ventas_app.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
