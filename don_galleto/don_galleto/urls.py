from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('panel/', include('panel.urls')),
    path('Receta/', include('Recetas_app.urls')) # SE AGREGO LA URL PARA LA RECETA HASTA SABER COMO SE VA HACER CON EL PANEL
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)