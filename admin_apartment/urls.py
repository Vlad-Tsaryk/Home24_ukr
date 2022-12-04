from django.urls import path
from .views import ApartmentCreate, ApartmentList, ApartmentUpdate, ApartmentView, apartment_delete

urlpatterns = [
    path('create/', ApartmentCreate.as_view(), name='apartment_create'),
    path('update/<pk>', ApartmentUpdate.as_view(), name='apartment_update'),
    path('<pk>', ApartmentView.as_view(), name='apartment_view'),
    path('delete/<pk>', apartment_delete, name='apartment_delete'),
    path('', ApartmentList.as_view(), name='apartment_list'),
]
