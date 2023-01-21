from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.messages import success, error
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from admin_apartment.models import Apartment
from admin_house.models import Section
from .forms import MeterForm, MeterUpdateForm
from .models import Meter
from admin_house.models import House
from admin_service.models import Service


# Create your views here.
class MeterView(DetailView):
    model = Meter
    template_name = 'admin_meter/meter_view.html'


class MeterCreate(SuccessMessageMixin, CreateView):
    model = Meter
    form_class = MeterForm
    template_name = 'admin_meter/meter_create.html'
    success_url = reverse_lazy('meter-list')
    success_message = 'Счетчик №%(number)s успешно создан'

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            result = {}
            house_id = self.request.GET.get('house_id')
            section_id = self.request.GET.get('section_id')
            print(self.request.GET)
            if house_id:
                if section_id:
                    result['apartment'] = list(Apartment.objects.filter(
                        house=house_id, section=section_id).values('id', 'number'))
                else:
                    result['apartment'] = list(Apartment.objects.filter(house_id=house_id).values('id', 'number'))
                    result['section'] = list(Section.objects.filter(house_id=house_id).values())
                print(result)
                return JsonResponse(result, safe=False, **response_kwargs)
        else:
            return super(CreateView, self).render_to_response(context, **response_kwargs)

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        if self.request.POST.get('action_save_add'):
            return redirect('meter-clone', pk=self.object.pk)
        return super().form_valid(form)


class MeterClone(MeterCreate):
    template_name = 'admin_meter/mater_clone.html'

    def get_form_kwargs(self):
        kwargs = super(MeterCreate, self).get_form_kwargs()
        try:
            meter_obj = get_object_or_404(Meter, pk=self.kwargs['pk'])
            self.kwargs['pk'] = meter_obj.pk
            meter_obj.pk = None
            meter_obj.apartment = None
            kwargs['instance'] = meter_obj
        except:
            pass
        return kwargs


class MeterNewValue(MeterCreate):
    template_name = 'admin_meter/meter_newValue.html'

    def get_form_kwargs(self):
        kwargs = super(MeterCreate, self).get_form_kwargs()
        try:
            apartment_obj = Apartment.objects.get(pk=self.kwargs['apartment_id'])
            self.kwargs['section_id'] = apartment_obj.section_id
            self.kwargs['house_id'] = apartment_obj.house_id
        except:
            pass
        return kwargs


class MeterList(ListView):
    model = Meter
    template_name = 'admin_meter/meter_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MeterList, self).get_context_data(**kwargs)
        context['house_list'] = House.objects.all()
        context['service_list'] = Service.objects.filter(is_counter=True)
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            order_by = self.request.GET.get('order_by')
            result = {}
            filter_fields = {
                'status': self.request.GET.get('status'),
                'apartment__house': self.request.GET.get('house'),
                'apartment__section_id': self.request.GET.get('section'),
                'apartment__number__contains': self.request.GET.get('apartment'),
                'service': self.request.GET.get('service'),
            }
            if self.request.GET.get('house_select'):
                result['sections'] = list(Section.objects.filter(house=filter_fields['apartment__house']).values())

            filter_fields = {k: v for k, v in filter_fields.items() if v}
            filtered_qs = self.get_queryset().filter(**filter_fields).order_by('service', 'apartment__number', '-pk')
            filtered_qs = filtered_qs.values('id', 'service', 'apartment', 'service__name', 'status',
                                             'apartment__house__name', 'apartment__section__name', 'value',
                                             'service__unit__name', 'apartment__number').distinct('service',
                                                                                                  'apartment__number')

            filtered_qs = list(filtered_qs)
            if order_by:
                if order_by[0] == '-':
                    filtered_qs = sorted(filtered_qs, key=lambda x: x[order_by[1:]], reverse=True)
                else:
                    filtered_qs = sorted(filtered_qs, key=lambda x: x[order_by])
            else:
                filtered_qs = sorted(filtered_qs, key=lambda x: x['id'], reverse=True)
            result['meter'] = filtered_qs
            print(result)
            return JsonResponse(result, safe=False, **response_kwargs)

        else:
            return super(ListView, self).render_to_response(context, **response_kwargs)


class MeterViewList(ListView):
    model = Meter
    template_name = 'admin_meter/meter_view_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MeterViewList, self).get_context_data(**kwargs)
        context['house_list'] = House.objects.all()
        context['service_list'] = Service.objects.filter(is_counter=True)
        return context

    def get_queryset(self):
        return Meter.objects.filter(apartment_id=self.kwargs['apartment_id'])

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            order_by = '-date'
            if self.request.GET.get('order_by'):
                order_by = self.request.GET.get('order_by')
            result = {}
            filter_fields = {
                'status': self.request.GET.get('status'),
                'number__contains': self.request.GET.get('number'),
                'apartment__house': self.request.GET.get('house'),
                'apartment__section_id': self.request.GET.get('section'),
                'apartment__number__contains': self.request.GET.get('apartment'),
                'service': self.request.GET.get('service'),
                'date__range': self.request.GET.getlist('date_range[]'),
            }
            print(self.request.GET)
            if self.request.GET.get('house_select'):
                result['sections'] = list(Section.objects.filter(house=filter_fields['apartment__house']).values())

            filter_fields = {k: v for k, v in filter_fields.items() if v}
            filtered_qs = self.get_queryset().filter(**filter_fields)
            filtered_qs = filtered_qs.values('id', 'date', 'service__name', 'status', 'apartment__house__name',
                                             'apartment__section__name', 'value', 'service__unit__name',
                                             'apartment__number', 'number')
            if order_by:
                filtered_qs = filtered_qs.order_by(order_by)
            filtered_qs = list(filtered_qs)
            result['meter'] = filtered_qs
            print(result)
            return JsonResponse(result, safe=False, **response_kwargs)

        else:
            return super(ListView, self).render_to_response(context, **response_kwargs)


class MeterUpdate(SuccessMessageMixin, UpdateView):
    model = Meter
    form_class = MeterUpdateForm
    template_name = 'admin_meter/meter_update.html'
    success_message = 'Счетчик №%(number)s успешно обновлен'

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            result = {}
            house_id = self.request.GET.get('house_id')
            section_id = self.request.GET.get('section_id')
            print(self.request.GET)
            if house_id:
                if section_id:
                    result['apartment'] = list(Apartment.objects.filter(
                        house=house_id, section=section_id).values('id', 'number'))
                else:
                    result['apartment'] = list(Apartment.objects.filter(house_id=house_id).values('id', 'number'))
                    result['section'] = list(Section.objects.filter(house_id=house_id).values())
                print(result)
                return JsonResponse(result, safe=False, **response_kwargs)
        else:
            return super(UpdateView, self).render_to_response(context, **response_kwargs)

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        if self.request.POST.get('action_save_add'):
            return redirect('meter-clone', pk=self.object.pk)
        return super().form_valid(form)

    def get_success_url(self):
        if self.object.service_id:
            return reverse_lazy('meter-view-list-serv',
                                kwargs={'apartment_id': self.object.apartment_id, 'service_id': self.object.service_id})
        else:
            return reverse_lazy('meter-view-list-apart',
                                kwargs={'apartment_id': self.object.apartment_id})


def meter_delete(request, pk):
    name = None
    apartment_id = None
    service_id = None
    try:
        obj_delete = Meter.objects.get(pk=pk)
        apartment_id = obj_delete.apartment_id
        service_id = obj_delete.service_id
        n = f'№{obj_delete.number}({obj_delete.service.name}) дом {obj_delete.apartment.house.name} ' \
            f',кв.{obj_delete.apartment.number} от {obj_delete.date}'
        if obj_delete.delete():
            name = n
    except:
        error(request, f"Не удалось удалить счетчик")
    if name:
        success(request, f"Показание {name} удален успешно")
    return redirect('meter-view-list-serv', apartment_id=apartment_id, service_id=service_id)
