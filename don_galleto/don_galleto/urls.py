from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('usuarios/', include('usuarios_app.urls')),
    path('panel/', include('panel.urls')),
    path('provedores/', include('provedores.urls')),
    path('ventas/', include('ventas_app.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
