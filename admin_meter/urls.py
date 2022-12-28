from django.urls import path
from .views import MeterCreate, MeterList, MeterClone

urlpatterns = [
    path('create/', MeterCreate.as_view(), name='meter_create'),
    path('create/clone_id=<pk>', MeterClone.as_view(), name='meter_clone'),
    path('', MeterList.as_view(), name='meter_list'),

]
