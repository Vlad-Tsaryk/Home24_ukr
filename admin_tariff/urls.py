from django.urls import path
from .views import TariffCreate

urlpatterns = [
    # path('', index, name='statistic'),
    path('create/', TariffCreate.as_view(), name='tariff_create'),

]
