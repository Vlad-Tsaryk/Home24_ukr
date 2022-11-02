from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, View, TemplateView, FormView
from .models import Service, Unit
from .forms import ServiceForm, ServiceFormSet, UnitFormSet, UnitForm


# Create your views here.
class ServiceEdit(TemplateView):
    # model = Service
    # form_class = ServiceForm
    success_url = reverse_lazy('service')
    template_name = 'admin_service/service_edit.html'

    def get_context_data(self, **kwargs):
        context = super(ServiceEdit, self).get_context_data(**kwargs)
        context['service_formset'] = ServiceFormSet(queryset=Service.objects.all(), prefix='service')
        context['unit_formset'] = UnitFormSet(queryset=Unit.objects.all(), prefix='unit')
        return context

    def post(self, request, *args, **kwargs):
        print(self.request.POST)
        service_formset = ServiceFormSet(self.request.POST or None, prefix='service')
        print(service_formset.errors)
        unit_formset = UnitFormSet(self.request.POST or None, prefix='unit')
        print(unit_formset.errors)
        if service_formset.is_valid() and unit_formset.is_valid():
            return self.form_valid(service_formset, unit_formset)

    def form_valid(self, service_formset, unit_formset):
        print('valid')
        service_formset.save(commit=False)
        for service in service_formset:
            service.save()
        unit_formset.save(commit=False)
        for unit in unit_formset:
            unit.save()
        return redirect(self.success_url)

    # def form_invalid(self, service_formset, unit_formset):
    #     print('invalid')
    #     return self.render_to_response(
    #         self.get_context_data(service_formset=service_formset,
    #                               unit_formset=unit_formset))

