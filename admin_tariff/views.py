from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView
from .models import Tariff, TariffService
from .forms import TariffForm, TariffServiceFormSet
from admin_service.models import Service
from django.contrib import messages


# Create your views here.
class TariffList(ListView):
    model = Tariff
    template_name = 'admin_tariff/tariff_list.html'


class TariffCreate(CreateView):
    model = Tariff
    form_class = TariffForm
    template_name = 'admin_tariff/tariff_create.html'
    success_url = 'tariff_list'

    def get_context_data(self, **kwargs):
        context = super(TariffCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['tariff_service_formset'] = TariffServiceFormSet(self.request.POST, prefix='tariff_service')
        else:
            context['tariff_service_formset'] = TariffServiceFormSet(prefix='tariff_service')
        context['service_list'] = Service.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        context = self.get_context_data()
        tariff_service_formset = context['tariff_service_formset']
        if tariff_service_formset.is_valid() and form.is_valid():
            return self.form_valid(form, tariff_service_formset)
        else:
            print(form.errors)
            print(tariff_service_formset.errors)

            print('invalid')
            return super(TariffCreate, self).render_to_response(self.get_context_data())

    def form_valid(self, form, formset):
        tariff = form.save()
        for tariff_service in formset:
            if tariff_service.cleaned_data['DELETE']:
                continue
            obj = tariff_service.save(commit=False)
            obj.tariff = tariff
            obj.save()
        messages.success(self.request, f"Тариф {tariff.name} создан успешно")
        return redirect(self.success_url)

class TariffUpdate(UpdateView):
    pass
