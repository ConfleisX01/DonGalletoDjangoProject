from django.urls import path, include
from main.views import main, welcome ,principal, panel
from django.conf.urls.static import static
from django.conf import settings
from clientes.views import ListaCarritoComprasView

urlpatterns = [
    path('', principal, name='home'),
    path('', main, name='home'),
    path('welcome/', welcome, name='welcome'),
    path("accounts/", include("django.contrib.auth.urls")),
    path("compras/", include('ventas_app.urls')),
    path("mi_carrito/", ListaCarritoComprasView.as_view(), name="carrito_de_compras")
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)