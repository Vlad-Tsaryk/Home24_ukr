from django.urls import path, include
from .views import HouseCreate, HouseList, HouseUpdate

urlpatterns = [
    path('create/', HouseCreate.as_view(), name='house_create'),
    path('update/<pk>', HouseUpdate.as_view(), name='house_update'),
    path('', HouseList.as_view(), name='house_list'),
]
