from django.shortcuts import render
from django.views.generic import ListView

from admin_apartment.models import Apartment
from admin_tariff.models import TariffService
from users.mixins import OwnerPermissionRequiredMixin


# Create your views here.
class ApartmentTariffView(OwnerPermissionRequiredMixin, ListView):
    model = TariffService
    template_name = 'cabinet_tariff/apartment_tariff_view.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ApartmentTariffView, self).get_context_data(**kwargs)
        context['apartment_name'] = Apartment.objects.get(pk=self.kwargs.get('pk')).info()
        return context

    def get_queryset(self):
        return TariffService.objects.select_related('tariff', 'service__unit').filter(tariff__apartment=self.kwargs.get('pk'))

