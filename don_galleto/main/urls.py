from django.urls import path, include
from main.views import main, welcome
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', main, name='home'),
    path('welcome', welcome, name='welcome'),
    path("accounts/", include("django.contrib.auth.urls")),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)