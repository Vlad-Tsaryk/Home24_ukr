from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView
from admin_personal_account.models import PersonalAccount
from admin_apartment.models import Apartment
from admin_house.models import Section
from admin_meter.models import Meter
from .forms import ReceiptForm, ReceiptServiceFormSet
from .models import Receipt, ReceiptService


# Create your views here.
class ReceiptCreate(CreateView):
    model = Receipt
    form_class = ReceiptForm
    template_name = 'admin_receipt/receipt_create.html'

    def get_context_data(self, **kwargs):
        context = super(ReceiptCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['receipt_service_formset'] = ReceiptServiceFormSet(self.request.POST, prefix='tariff_service')
        else:
            context['receipt_service_formset'] = ReceiptServiceFormSet(prefix='tariff_service',
                                                                       queryset=ReceiptService.objects.none())
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            result = {}
            house_id = self.request.GET.get('house_id')
            section_id = self.request.GET.get('section_id')
            apartment_id = self.request.GET.get('apartment_id')
            personal_account = self.request.GET.get('personal_account')
            print(self.request.GET)
            if apartment_id or personal_account:
                if apartment_id:
                    apartment_obj = Apartment.objects.get(pk=apartment_id)
                else:
                    apartment_obj = PersonalAccount.objects.get(number=personal_account).apartment
                    result['apartment'] = list(Apartment.objects.filter(house_id=apartment_obj.house_id,
                                                                        section_id=apartment_obj.section_id).values(
                        'id', 'number'))
                    result['section'] = list(Section.objects.filter(house_id=apartment_obj.house_id).values())

                apartment_info = {
                    'owner': str(apartment_obj.owner),
                    'owner_id': apartment_obj.owner_id,
                    'owner_phone': str(apartment_obj.owner.phone),
                    'tariff_id': apartment_obj.tariff_id,
                    'house_id': apartment_obj.house_id,
                    'section_id': apartment_obj.section_id,
                    'apartment_id': apartment_obj.id,
                }
                try:
                    apartment_info['personal_account'] = PersonalAccount.objects.get(apartment=apartment_id).number
                except:
                    pass
                result['meter_list'] = list(Meter.objects.order_by('-date').filter(
                    apartment_id=apartment_obj.id).values('number', 'status', 'date', 'apartment__house__name',
                                                          'apartment__number', 'apartment__section__name',
                                                          'service__name', 'value', 'service__unit__name'))
                result['apartment_info'] = apartment_info
                print(result)
            elif house_id:
                if section_id:
                    result['apartment'] = list(Apartment.objects.filter(
                        house=house_id, section=section_id).values('id', 'number'))
                else:
                    result['apartment'] = list(Apartment.objects.filter(house_id=house_id).values('id', 'number'))
                    result['section'] = list(Section.objects.filter(house_id=house_id).values())
                print(result)
            if not self.request.GET.get('meter_set'):
                result['meter_list'] = list(
                    Meter.objects.order_by('-date').values('number', 'status', 'date', 'apartment__house__name',
                                                           'apartment__number', 'apartment__section__name',
                                                           'service__name', 'value', 'service__unit__name'))
            return JsonResponse(result, safe=False, **response_kwargs)

        else:
            return super(ReceiptCreate, self).render_to_response(context, **response_kwargs)
