from django.shortcuts import render
from django.views.generic import ListView

from admin_tariff.models import TariffService


# Create your views here.
class ApartmentTariffView(ListView):
    model = TariffService
    template_name = 'cabinet_tariff/apartment_tariff_view.html'

    def get_queryset(self):
        return TariffService.objects.select_related('tariff', 'service__unit').filter(tariff__apartment=self.kwargs.get('pk'))

