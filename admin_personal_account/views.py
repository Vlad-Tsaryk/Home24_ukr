from django.db.models import Value
from django.db.models.functions import Concat
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.contrib import messages
from admin_house.models import House
from .models import PersonalAccount
from .forms import PersonalAccountForm
from admin_apartment.models import Apartment, Section


# Create your views here.

class PersonalAccountView(DetailView):
    model = PersonalAccount
    template_name = 'admin_personal_account/personal_account_view.html'


class PersonalAccountCreate(CreateView):
    model = PersonalAccount
    form_class = PersonalAccountForm
    template_name = 'admin_personal_account/personal_account_create.html'
    success_url = reverse_lazy('personal_account_list')

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


class PersonalAccountUpdate(UpdateView):
    model = PersonalAccount
    template_name = 'admin_personal_account/personal_account_update.html'
    form_class = PersonalAccountForm
    success_url = reverse_lazy('personal_account_list')


def personal_account_delete(request, pk):
    number = None
    try:
        obj_delete = PersonalAccount.objects.get(pk=pk)
        n = obj_delete.__str__()
        if obj_delete.delete():
            number = n
    except:
        messages.error(request, f"Не удалось удалить лицевой счет")
    if number:
        messages.success(request, f"Лицевой счет №{number} удален успешно")
    return redirect('personal_account_list')


class PersonalAccountList(ListView):
    model = PersonalAccount
    template_name = 'admin_personal_account/personal_account_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PersonalAccountList, self).get_context_data(**kwargs)
        context['house_list'] = House.objects.all()
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            print(self.request.GET)
            result = {}
            filter_fields = {
                'number__contains': self.request.GET.get('number'),
                'status': self.request.GET.get('status'),
                'apartment__house': self.request.GET.get('house'),
                'apartment__section_id': self.request.GET.get('section'),
                'apartment__number__contains': self.request.GET.get('apartment'),
                'apartment__owner': self.request.GET.get('owner'),
            }
            if self.request.GET.get('house_select'):
                result['sections'] = list(Section.objects.filter(house=filter_fields['apartment__house']).values())

            filter_fields = {k: v for k, v in filter_fields.items() if v}
            filtered_qs = self.get_queryset().filter(**filter_fields)
            filtered_qs = filtered_qs.annotate(
                owner__name=Concat('apartment__owner__first_name', Value(' '),
                                   'apartment__owner__middle_name', Value(' '),
                                   'apartment__owner__last_name'))
            has_debt_list = [personal_account.balance for personal_account in filtered_qs]
            filtered_qs = list(
                filtered_qs.values('id', 'number', 'status', 'apartment__house__name', 'apartment__number',
                                   'apartment__section__name', 'owner__name'))
            for index, personal_account in enumerate(filtered_qs):
                personal_account['balance'] = has_debt_list[index]
            result['account'] = filtered_qs
            print(result)
            return JsonResponse(result, safe=False, **response_kwargs)

        else:
            return super(ListView, self).render_to_response(context, **response_kwargs)
