from django.urls import path
from .views import MeterCreate, MeterList, MeterClone, MeterNewValue, MeterViewList, MeterUpdate

urlpatterns = [
    path('create/', MeterCreate.as_view(), name='meter_create'),
    path('update/<pk>', MeterUpdate.as_view(), name='meter_update'),
    path('create/clone_id=<pk>', MeterClone.as_view(), name='meter_clone'),
    # path('create/apartment_id=<apartment_id>', MeterNewValue.as_view(), name='meter_new_value'),
    path('create/apartment=<apartment_id>_service=<service_id>', MeterNewValue.as_view(), name='meter_new_value'),
    # path('create/apartment=<apartment_id>', MeterNewValue.as_view(), name='meter_new_value'),
    path('meter_list/apartment=<apartment_id>_service=<service_id>', MeterViewList.as_view(), name='meter_view_list'),
    path('', MeterList.as_view(), name='meter_list'),

]
