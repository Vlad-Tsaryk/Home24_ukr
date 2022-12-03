from django.urls import path, include
from .views import ApartmentCreate, ApartmentList, ApartmentUpdate

urlpatterns = [
    path('create/', ApartmentCreate.as_view(), name='apartment_create'),
    path('update/<pk>', ApartmentUpdate.as_view(), name='apartment_update'),
    path('', ApartmentList.as_view(), name='apartment_list'),
]
