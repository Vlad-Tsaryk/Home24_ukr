from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, DetailView

from admin_service.models import Service
from users.mixins import AdminPermissionRequiredMixin
from .forms import TariffForm, TariffServiceFormSet
from .models import Tariff, TariffService


# Create your views here.
class TariffList(AdminPermissionRequiredMixin, ListView):
    permission_required = 'tariffs'
    model = Tariff
    template_name = 'admin_tariff/tariff_list.html'


class TariffCreate(AdminPermissionRequiredMixin, CreateView):
    permission_required = 'tariffs'
    model = Tariff
    form_class = TariffForm
    template_name = 'admin_tariff/tariff_create.html'
    success_url = 'tariff_list'

    def get_context_data(self, **kwargs):
        context = super(TariffCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['tariff_service_formset'] = TariffServiceFormSet(self.request.POST, prefix='tariff_service')
        else:
            context['tariff_service_formset'] = TariffServiceFormSet(prefix='tariff_service',
                                                                     queryset=TariffService.objects.none())
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
            return super(TariffCreate, self).render_to_response(self.get_context_data())

    def form_valid(self, form, formset):
        tariff = form.save()
        tariff_service_formset = formset.save(commit=False)
        for tariff_service in tariff_service_formset:
            tariff_service.tariff = tariff
        formset.save()
        messages.success(self.request, f"Тариф {tariff.name} создан успішно")
        return redirect(self.success_url)


class TariffClone(TariffCreate):
    def get_form_kwargs(self):
        kwargs = super(TariffCreate, self).get_form_kwargs()
        if self.kwargs['pk']:
            tariff_obj = get_object_or_404(Tariff, pk=self.kwargs['pk'])
            tariff_obj.pk = None
            kwargs['instance'] = tariff_obj
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(TariffCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['tariff_service_formset'] = TariffServiceFormSet(self.request.POST, prefix='tariff_service')
        else:
            formset = TariffServiceFormSet(prefix='tariff_service',
                                           queryset=TariffService.objects.filter(tariff_id=self.kwargs['pk']))
            formset.management_form.initial['INITIAL_FORMS'] = 0
            context['tariff_service_formset'] = formset
        context['service_list'] = Service.objects.all()
        return context


class TariffUpdate(AdminPermissionRequiredMixin, UpdateView):
    permission_required = 'tariffs'
    model = Tariff
    form_class = TariffForm
    template_name = 'admin_tariff/tariff_update.html'
    success_url = 'tariff_list'

    def get_context_data(self, **kwargs):
        context = super(TariffUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['tariff_service_formset'] = TariffServiceFormSet(self.request.POST, prefix='tariff_service')
        else:
            context['tariff_service_formset'] = TariffServiceFormSet(prefix='tariff_service',
                                                                     queryset=TariffService.objects.filter(
                                                                         tariff_id=self.kwargs['pk']))
        context['service_list'] = Service.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        context = self.get_context_data()
        tariff_service_formset = context['tariff_service_formset']
        if tariff_service_formset.is_valid() and form.is_valid():
            return self.form_valid(form, tariff_service_formset)
        else:
            return super(TariffUpdate, self).render_to_response(self.get_context_data())

    def form_valid(self, form, formset):
        tariff = form.save()
        tariff_service_formset = formset.save(commit=False)
        for tariff_service in tariff_service_formset:
            tariff_service.tariff = tariff
        formset.save()
        messages.success(self.request, f"Тариф {tariff.name} обновлен успішно")
        return redirect(self.success_url)


class TariffView(AdminPermissionRequiredMixin, DetailView):
    permission_required = 'tariffs'
    model = Tariff
    template_name = 'admin_tariff/tariff_view.html'


def delete_tariff(request, pk):
    obj_tariff = get_object_or_404(Tariff, pk=pk)
    messages.success(request, f"Тариф {obj_tariff.name} успішно удалён")
    obj_tariff.delete()

    return redirect('tariff_list')
