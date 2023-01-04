from django.urls import path
from .views import MeterCreate, MeterList, MeterClone, MeterNewValue, MeterView

urlpatterns = [
    path('create/', MeterCreate.as_view(), name='meter_create'),
    path('create/clone_id=<pk>', MeterClone.as_view(), name='meter_clone'),
    path('create/meter=<pk>', MeterNewValue.as_view(), name='meter_new_value'),
    path('meter_list/apartment=<apartment_id>&service=<service_id>', MeterView.as_view(), name='meter_view'),
    path('', MeterList.as_view(), name='meter_list'),

]
