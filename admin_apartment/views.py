from django.db.models.functions import Concat
from django.db.models import Value
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from .models import Apartment, Section, Floor, House
from .forms import ApartmentForm


# Create your views here.

def apartment_house_details(house_id, **response_kwargs):
    section_list = list(Section.objects.filter(house=house_id).values())
    floor_list = list(Floor.objects.filter(house=house_id).values())
    return JsonResponse({'section': section_list, 'floor': floor_list}, safe=False, **response_kwargs)


class ApartmentCreate(CreateView):
    model = Apartment
    template_name = 'admin_apartment/apartment_create.html'
    form_class = ApartmentForm
    success_url = reverse_lazy('apartment_list')

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            house_id = self.request.GET.get('house_id')
            if house_id:
                return apartment_house_details(house_id, **response_kwargs)
        else:
            return super(CreateView, self).render_to_response(context, **response_kwargs)


class ApartmentUpdate(UpdateView):
    model = Apartment
    template_name = 'admin_apartment/apartment_update.html'
    form_class = ApartmentForm
    success_url = reverse_lazy('apartment_list')

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            house_id = self.request.GET.get('house_id')
            if house_id:
                return apartment_house_details(house_id, **response_kwargs)
        else:
            return super(UpdateView, self).render_to_response(context, **response_kwargs)

class ApartmentList(ListView):
    model = Apartment
    template_name = 'admin_apartment/apartment_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ApartmentList, self).get_context_data(**kwargs)
        context['house_list'] = House.objects.all()
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            print(self.request.GET)
            result = {'apartment': ''}
            filter_fields = {
                'number': self.request.GET.get('number'),
                'house': self.request.GET.get('house'),
                'section': self.request.GET.get('section'),
                'floor': self.request.GET.get('floor'),
                'owner': self.request.GET.get('owner'),
            }
            if self.request.GET.get('house_select'):
                result['sections'] = list(Section.objects.filter(house=filter_fields['house']).values())
                result['floors'] = list(Floor.objects.filter(house=filter_fields['house']).values())

            filter_fields = {k: v for k, v in filter_fields.items() if v}
            filtered_qs = self.get_queryset().filter(**filter_fields)
            order_field = self.request.GET.get('order_by')
            filtered_qs = filtered_qs.annotate(
                owner__name=Concat('owner__first_name', Value(' '),
                                   'owner__middle_name', Value(' '),
                                   'owner__last_name'))
            if order_field:
                filtered_qs = filtered_qs.order_by(order_field)
            result['apartment'] = list(
                filtered_qs.values('id', 'number', 'house__name', 'floor__name', 'section__name', 'owner__name'))
            return JsonResponse(result, safe=False, **response_kwargs)

        else:
            return super(ListView, self).render_to_response(context, **response_kwargs)
