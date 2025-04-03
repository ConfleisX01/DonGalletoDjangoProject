from django.contrib import admin
from main.views import principal, panel
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from two_factor.urls import urlpatterns as tf_urls

from main import views

urlpatterns = [
    path('superduper_adminpanel/', admin.site.urls),
    path('', include('main.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # URLs estándar de Django
    path('accounts/', include(tf_urls)),  # URLs de autenticación en dos pasos
    path('accounts/registro/', views.registro, name="registro"),
    path('panel', panel, name='panel'),
    path('principal', principal, name='principal'),
    path('usuarios/', include('usuarios_app.urls')),
    path('panel/', include('panel.urls')),
    path('provedores/', include('provedores.urls')),
    path('materia_prima/', include('materia_prima.urls')),
    path('recetas/', include('Recetas_app.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
