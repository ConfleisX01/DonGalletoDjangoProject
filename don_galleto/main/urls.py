from django.urls import path
from main.views import main, welcome

urlpatterns = [
    path('', main, name='home'),
    path('welcome/', welcome, name='welcome' )
]