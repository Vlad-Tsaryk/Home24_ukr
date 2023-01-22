from django.db.models.functions import Concat
from django.db.models import Value, CharField
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from admin_personal_account.models import PersonalAccount
from admin_apartment.models import Apartment
from admin_house.models import Section
from admin_meter.models import Meter
from admin_tariff.models import Tariff, TariffService
from .forms import ReceiptForm, ReceiptServiceFormSet
from .models import Receipt, ReceiptService
from users.models import User, Role


# Create your views here.
class ReceiptCreate(CreateView):
    model = Receipt
    form_class = ReceiptForm
    template_name = 'admin_receipt/receipt_create.html'
    success_url = reverse_lazy('receipt_list')

    def get_context_data(self, **kwargs):
        context = super(ReceiptCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['receipt_service_formset'] = ReceiptServiceFormSet(self.request.POST, prefix='receipt_service')
        else:
            context['receipt_service_formset'] = ReceiptServiceFormSet(prefix='receipt_service',
                                                                       queryset=ReceiptService.objects.none())
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        context = self.get_context_data()
        receipt_service_formset = context['receipt_service_formset']
        if receipt_service_formset.is_valid() and form.is_valid():
            return self.form_valid(form, receipt_service_formset)
        else:
            return super(ReceiptCreate, self).render_to_response(self.get_context_data())

    def form_valid(self, form, formset):
        receipt = form.save()
        receipt_service_formset = formset.save(commit=False)
        for receipt_service in receipt_service_formset:
            receipt_service.receipt = receipt
        formset.save()
        return super().form_valid(form)

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            result = {}
            house_id = self.request.GET.get('house_id')
            section_id = self.request.GET.get('section_id')
            apartment_id = self.request.GET.get('apartment_id')
            personal_account = self.request.GET.get('personal_account')
            tariff_id = self.request.GET.get('tariff')
            print(self.request.GET)
            if self.request.GET.get('set_tariff_services'):
                if tariff_id:
                    result['tariff_services'] = list(TariffService.objects.filter(tariff=tariff_id).values('service_id',
                                                                                                           'price'))
            if self.request.GET.get('set_meter_values'):
                if apartment_id:
                    meter_new_val = Meter.objects.filter(apartment=apartment_id, status=Meter.StatusName.NEW)
                    # result['tariff_meter_values'] = Meter.objects.filter(status=)
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


class ReceiptList(ListView):
    model = Receipt
    template_name = 'admin_receipt/receipt_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ReceiptList, self).get_context_data(**kwargs)
        context['owner_list'] = User.objects.filter(role__role=Role.RoleName.OWNER)
        context['status_list'] = Receipt.StatusName.values
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            order_by = self.request.GET.get('order_by')
            print(self.request.GET)
            result = {}
            filter_fields = {
                'status': self.request.GET.get('status'),
                'number__contains': self.request.GET.get('number'),
                'apartment_info__contains': self.request.GET.get('apartment'),
                'apartment__owner_id': self.request.GET.get('owner'),
                'is_complete': self.request.GET.get('is_complete'),
                'date__range': self.request.GET.getlist('date_range[]'),
                'date__month': self.request.GET.get('date_month'),
                'date__year': self.request.GET.get('date_year'),
            }
            filter_fields = {k: v for k, v in filter_fields.items() if v}
            filtered_qs = self.get_queryset().annotate(
                apartment_info=Concat(Value('Квартира №'), 'apartment__number', Value(', '),
                                      'apartment__house__name', output_field=CharField()),
            ).filter(**filter_fields)
            if order_by:
                filtered_qs = filtered_qs.order_by(order_by)
            total_price_list = [receipt.total_price for receipt in filtered_qs]
            filtered_qs = filtered_qs.values('id', 'date', 'apartment_info', 'status', 'number',
                                             'apartment__owner__first_name', 'apartment__owner__last_name',
                                             'apartment__owner__middle_name', 'apartment__owner_id',
                                             'is_complete')
            for index, receipt in enumerate(filtered_qs):
                receipt['total_price'] = total_price_list[index]
            print(filtered_qs)
            result['receipts'] = list(filtered_qs)
            print(result)
            return JsonResponse(result, safe=False, **response_kwargs)

        else:
            return super(ListView, self).render_to_response(context, **response_kwargs)
