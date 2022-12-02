from django.urls import path, include
from .views import ApartmentCreate, ApartmentList

urlpatterns = [
    path('create/', ApartmentCreate.as_view(), name='apartment_create'),
    path('', ApartmentList.as_view(), name='apartment_list'),
]
