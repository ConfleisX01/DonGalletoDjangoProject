from django.contrib import admin
from main.views import principal, panel, welcome
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('accounts/', include("django.contrib.auth.urls")),
    path('accounts/registro/', views.registro, name="registro"),
    path('panel', panel, name='panel'),
    path('principal', principal, name='principal'),
    path('welcome', welcome, name='welcome'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
