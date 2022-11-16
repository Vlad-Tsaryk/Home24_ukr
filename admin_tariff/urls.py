from django.urls import path
from .views import TariffCreate, TariffList

urlpatterns = [
    path('', TariffList.as_view(), name='tariff_list'),
    path('create/', TariffCreate.as_view(), name='tariff_create'),

]
