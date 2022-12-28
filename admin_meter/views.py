from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from admin_apartment.models import Apartment
from admin_house.models import Section
from .forms import MeterForm
from .models import Meter


# Create your views here.
class MeterCreate(CreateView):
    model = Meter
    form_class = MeterForm
    template_name = 'admin_meter/meter_create.html'

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            house_id = self.request.GET.get('house_id')
            section_id = self.request.GET.get('section_id')
            if house_id:
                if section_id:
                    result = {'apartment': list(Apartment.objects.filter(
                        house=house_id, section=section_id).values('id', 'number'))}
                else:
                    result = {'apartment': list(Apartment.objects.filter(
                        house_id=house_id).values('id', 'number')),
                              'section': list(Section.objects.filter(house_id=house_id).values())}
                print(result)
                return JsonResponse(result, safe=False, **response_kwargs)
        else:
            return super(CreateView, self).render_to_response(context, **response_kwargs)


class MeterList(ListView):
    model = Meter
    template_name = 'admin_meter/meter_list.html'
