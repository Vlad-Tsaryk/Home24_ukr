from django.urls import path, include
from .views import HouseCreate, HouseList, HouseUpdate, HouseView, house_delete

urlpatterns = [
    path('create/', HouseCreate.as_view(), name='house_create'),
    path('update/<pk>', HouseUpdate.as_view(), name='house_update'),
    path('<pk>', HouseView.as_view(), name='house_view'),
    path('delete/<pk>', house_delete, name='house_delete'),
    path('', HouseList.as_view(), name='house_list'),
]
