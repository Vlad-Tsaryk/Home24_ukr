from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, View, TemplateView, FormView
from .models import Service, Unit
from .forms import ServiceForm, ServiceFormSet, UnitFormSet, UnitForm


# Create your views here.
class ServiceEdit(TemplateView):
    success_url = reverse_lazy('service')
    template_name = 'admin_service/service_edit.html'

    def get_context_data(self, **kwargs):
        context = super(ServiceEdit, self).get_context_data(**kwargs)
        if self.request.POST:
            context['service_formset'] = ServiceFormSet(self.request.POST, prefix='service')
            context['unit_formset'] = UnitFormSet(self.request.POST, prefix='unit')
        else:
            context['service_formset'] = ServiceFormSet(queryset=Service.objects.all(), prefix='service')
            context['unit_formset'] = UnitFormSet(queryset=Unit.objects.all(), prefix='unit')

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        service_formset = context['service_formset']
        unit_formset = context['unit_formset']
        return self.form_valid(service_formset, unit_formset)

    def form_valid(self, service_formset, unit_formset):
        if service_formset.is_valid() and unit_formset.is_valid():
            print('valid')
            service_formset.save()
            unit_formset.save()
            return redirect(self.success_url)
        else:
            print('invalid')



    # def form_invalid(self, service_formset, unit_formset):
    #     print('invalid')
    #     return self.render_to_response(
    #         self.get_context_data(service_formset=service_formset,
    #                               unit_formset=unit_formset))

