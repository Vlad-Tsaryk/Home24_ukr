from django.urls import path, include
from .views import HouseCreate

urlpatterns = [
    path('create/',HouseCreate.as_view(), name='house_create')
]