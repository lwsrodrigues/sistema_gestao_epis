from django.urls import path
from .views import home

urlpatterns = [
    path('', home),  # Quando acessar "/", vai chamar a função home
]
