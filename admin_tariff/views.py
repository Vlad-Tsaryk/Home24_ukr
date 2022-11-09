from django.shortcuts import render, redirect
from django.views.generic import CreateView
from .models import Tariff, TariffService
from .forms import TariffForm, TariffServiceFormSet
from admin_service.models import Service


# Create your views here.
class TariffCreate(CreateView):
    model = Tariff
    form_class = TariffForm
    template_name = 'admin_tariff/tariff_create.html'

    def get_context_data(self, **kwargs):
        context = super(TariffCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['tariff_service_formset'] = TariffServiceFormSet(self.request.POST, prefix='tariff_service')
        else:
            context['tariff_service_formset'] = TariffServiceFormSet(prefix='tariff_service')
        context['service_list'] = Service.objects.all()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        tariff_service_formset = context['tariff_service_formset']
        if tariff_service_formset.is_valid() and form.is_valid():
            formset = tariff_service_formset.save(commit=False)
            for tariff_service in formset:
                tariff_service
            unit_formset.save()
            return redirect(self.success_url)
        else:
            return super(TariffCreate, self).render_to_response(self.get_context_data())
