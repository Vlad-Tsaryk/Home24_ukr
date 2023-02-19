from django.urls import path
from .views import ApartmentTariffView

urlpatterns = [
    path('apartment_id=<pk>', ApartmentTariffView.as_view(), name='cabinet_apartment_tariff_view'),
]
