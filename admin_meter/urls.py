from django.urls import path
from .views import MeterCreate, MeterList, MeterClone, MeterNewValue, MeterViewList

urlpatterns = [
    path('create/', MeterCreate.as_view(), name='meter_create'),
    path('create/clone_id=<pk>', MeterClone.as_view(), name='meter_clone'),
    path('create/meter=<pk>', MeterNewValue.as_view(), name='meter_new_value'),
    path('meter_list/apartment=<apartment_id>_service=<service_id>', MeterViewList.as_view(), name='meter_view_list'),
    path('', MeterList.as_view(), name='meter_list'),
    path('', MeterList.as_view(), name='meter_list'),

]
