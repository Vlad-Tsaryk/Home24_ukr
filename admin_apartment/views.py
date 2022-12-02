from django.db.models.functions import Concat
from django.db.models import Value
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from .models import Apartment, Section, Floor, House
from .forms import ApartmentForm


# Create your views here.


class ApartmentCreate(CreateView):
    model = Apartment
    template_name = 'admin_apartment/apartment_create.html'
    form_class = ApartmentForm

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            print(self.request.GET)
            house_id = self.request.GET.get('house_id')
            if house_id:
                print(Section.objects.filter(house=house_id).values())
                section_list = list(Section.objects.filter(house=house_id).values())
                floor_list = list(Floor.objects.filter(house=house_id).values())
                print(section_list)
                print(floor_list)
                return JsonResponse({'section': section_list, 'floor': floor_list}, safe=False, **response_kwargs)
        else:
            return super(CreateView, self).render_to_response(context, **response_kwargs)


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
            filter_fields = {
                'number': self.request.GET.get('number'),
                'house': self.request.GET.get('house'),
                'section': self.request.GET.get('section'),
                'floor': self.request.GET.get('floor'),
                'owner': self.request.GET.get('owner'),
            }
            filter_fields = {k: v for k, v in filter_fields.items() if v}
            filtered_qs = self.get_queryset().filter(**filter_fields)
            order_field = self.request.GET.get('order_by')
            filtered_qs = filtered_qs.annotate(
                owner__name=Concat('owner__first_name', Value(' '),
                                   'owner__middle_name', Value(' '),
                                   'owner__last_name'))
            if order_field:
                filtered_qs = filtered_qs.order_by(order_field)
            result_list = list(
                filtered_qs.values('id', 'number', 'house__name', 'floor__name', 'section__name', 'owner__name'))

            print(result_list)
            return JsonResponse(result_list, safe=False, **response_kwargs)

        else:
            return super(ListView, self).render_to_response(context, **response_kwargs)
