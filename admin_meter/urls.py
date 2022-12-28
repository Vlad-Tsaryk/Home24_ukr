from django.urls import path
from .views import MeterCreate, MeterList

urlpatterns = [
    path('create/', MeterCreate.as_view(), name='meter_create'),
    path('', MeterList.as_view(), name='meter_list'),
]
