from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from .models import PersonalAccount
from .forms import PersonalAccountForm
from admin_apartment.models import Apartment, Section


# Create your views here.
class PersonalAccountCreate(CreateView):
    model = PersonalAccount
    form_class = PersonalAccountForm
    template_name = 'admin_personal_account/personal_account_create.html'

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            house_id = self.request.GET.get('house_id')
            section_id = self.request.GET.get('section_id')
            print(self.request.GET)
            if house_id:
                if section_id:
                    result = {'apartment': list(Apartment.objects.filter(
                        house=house_id, section=section_id).values('id', 'number', 'owner__first_name', 'owner',
                                                                   'owner__middle_name', 'owner__last_name',
                                                                   'owner__phone'))}
                else:
                    result = {'apartment': list(Apartment.objects.filter(
                        house_id=house_id).values('id', 'number', 'owner__first_name', 'owner__phone',
                                                  'owner__middle_name', 'owner__last_name', 'owner')),
                              'section': list(Section.objects.filter(house_id=house_id).values())}
                print(result)
                return JsonResponse(result, safe=False, **response_kwargs)
        else:
            return super(CreateView, self).render_to_response(context, **response_kwargs)


class PersonalAccountList(ListView):
    model = PersonalAccount
    template_name = 'admin_personal_account/personal_account_list.html'
