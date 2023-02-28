from django.core.paginator import Paginator
from django.db.models.functions import Concat
from django.db.models import Value, CharField, F
from django.http import JsonResponse
from django.contrib.messages import success, error
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from admin_personal_account.models import PersonalAccount
from admin_apartment.models import Apartment
from admin_house.models import Section
from admin_meter.models import Meter
from admin_personal_account.utils import PersonalAccountBalance
from admin_tariff.models import TariffService
from admin_transaction.models import Transaction
from users.mixins import AdminPermissionRequiredMixin
from .forms import ReceiptForm, ReceiptServiceFormSet
from .models import Receipt, ReceiptService
from users.models import User, Role


# Create your views here.
class ReceiptCreate(AdminPermissionRequiredMixin, CreateView):
    permission_required = 'receipts'
    model = Receipt
    form_class = ReceiptForm
    template_name = 'admin_receipt/receipt_create.html'
    success_url = reverse_lazy('receipt_list')
    success_message = 'создана'

    def get_context_data(self, **kwargs):
        context = super(ReceiptCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['receipt_service_formset'] = ReceiptServiceFormSet(self.request.POST, prefix='receipt_service')
        else:
            context['receipt_service_formset'] = ReceiptServiceFormSet(prefix='receipt_service',
                                                                       queryset=ReceiptService.objects.none())
        return context

    def get_post_object(self):
        self.object = None

    def post(self, request, *args, **kwargs):
        self.get_post_object()
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
        receipt.set_total_price()
        success(self.request, f'Квитанция {receipt.number} {self.success_message} успешно')
        return super().form_valid(form)

    def get_meters_consumption(self):
        metest = Meter.objects.filter(apartment_id=self.request.GET.get('apartment_id')) \
            .order_by('service', 'status', '-pk', ) \
            .distinct('service', 'status')
        metest_new = metest.filter(status=Meter.StatusName.NEW)
        metest_clarified = metest
        meters_consumption = {}
        for meter in metest_new:
            try:
                value = meter.value - metest_clarified.filter(service=meter.service).last().value
            except Meter.DoesNotExist:
                meters_consumption[meter.service_id] = meter.value
                continue
            if value < 0:
                value = None
            meters_consumption[meter.service_id] = value
        return meters_consumption

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
                result['meters_consumption'] = self.get_meters_consumption()
                # if apartment_id:
                #     meter_new_val = Meter.objects.filter(apartment=apartment_id, status=Meter.StatusName.NEW)
                #     # result['tariff_meter_values'] = Meter.objects.filter(status=)
            if apartment_id or personal_account:
                if apartment_id:
                    apartment_obj = Apartment.objects.get(pk=apartment_id)
                else:
                    apartment_obj = PersonalAccount.objects.get(number=personal_account).apartment
                    result['apartment'] = list(Apartment.objects.filter(house_id=apartment_obj.house_id,
                                                                        section_id=apartment_obj.section_id,
                                                                        personalaccount__isnull=False).values(
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
                result['meter_list'] = list(Meter.objects.order_by('-date', '-number').filter(
                    apartment_id=apartment_obj.id).values('number', 'status', 'date', 'apartment__house__name',
                                                          'apartment__number', 'apartment__section__name',
                                                          'service__name', 'value', 'service__unit__name'))
                result['apartment_info'] = apartment_info
                print(result)
            elif house_id:
                if section_id:
                    result['apartment'] = list(Apartment.objects.filter(
                        house=house_id, section=section_id, personalaccount__isnull=False).values('id', 'number'))
                else:
                    result['apartment'] = list(Apartment.objects.filter(house_id=house_id,
                                                                        personalaccount__isnull=False).values('id',
                                                                                                              'number'))
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


class ReceiptUpdate(ReceiptCreate, UpdateView):
    template_name = 'admin_receipt/receipt_update.html'
    success_message = 'обновлена'

    def get_context_data(self, **kwargs):
        context = super(ReceiptUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['receipt_service_formset'] = ReceiptServiceFormSet(self.request.POST, prefix='receipt_service')
        else:
            context['receipt_service_formset'] = ReceiptServiceFormSet(prefix='receipt_service',
                                                                       queryset=ReceiptService.objects.filter(
                                                                           receipt_id=self.kwargs['pk']))
        return context

    def get_post_object(self):
        self.object = self.get_object()


class ReceiptList(AdminPermissionRequiredMixin, ListView):
    permission_required = 'receipts'
    model = Receipt
    template_name = 'admin_receipt/receipt_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ReceiptList, self).get_context_data(**kwargs)
        context['owner_list'] = User.objects.filter(role__role=Role.RoleName.OWNER)
        context['status_list'] = Receipt.StatusName.values
        context['account_total_debt'] = PersonalAccountBalance.get_total_debt()
        context['account_total_balance'] = PersonalAccountBalance.get_total_balance()
        context['transactions_total_balance'] = Transaction.total_balance()
        return context

    def delete_receipts(self):
        delete_info = {
            'success_msg': [],
            'error_msg': [],
        }
        for pk in self.request.GET.getlist('selected_receipts[]'):
            obj_number = None
            try:
                obj_delete = Receipt.objects.get(pk=pk)
                obj_number = obj_delete.number
                if obj_delete.delete():
                    delete_info['success_msg'].append(f"Квитанция №{obj_number} успешно удалена")
            except:
                delete_info['error_msg'].append(f"Не удалось удалить квитанцию №{obj_number}")
        return delete_info

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            result = {}
            if self.request.GET.get('delete_receipts'):
                result['delete_info'] = self.delete_receipts()
            order_by = self.request.GET.get('order_by')
            print(self.request.GET)
            filter_fields = {
                'status': self.request.GET.get('status'),
                'number__contains': self.request.GET.get('number'),
                'apartment_info__contains': self.request.GET.get('apartment'),
                'personal_account__apartment__owner_id': self.request.GET.get('owner'),
                'is_complete': self.request.GET.get('is_complete'),
                'date__range': self.request.GET.getlist('date_range[]'),
                'date__month': self.request.GET.get('date_month'),
                'date__year': self.request.GET.get('date_year'),
            }
            filter_fields = {k: v for k, v in filter_fields.items() if v}
            filtered_qs = self.get_queryset().annotate(
                apartment_info=Concat(Value('Квартира №'), 'personal_account__apartment__number', Value(', '),
                                      'personal_account__apartment__house__name', output_field=CharField()),
            ).filter(**filter_fields)
            if order_by:
                filtered_qs = filtered_qs.order_by(order_by)
            filtered_qs = filtered_qs.values('id', 'date', 'apartment_info', 'status', 'number',
                                             'personal_account__apartment__owner__first_name',
                                             'personal_account__apartment__owner__last_name',
                                             'personal_account__apartment__owner__middle_name',
                                             'personal_account__apartment__owner_id',
                                             'is_complete', 'total_price')
            start = int(self.request.GET.get('start', 0))
            length = int(self.request.GET.get('length', 10))
            paginator = Paginator(filtered_qs, self.request.GET.get('length', 10))
            page = (start // length) + 1
            data = list(paginator.get_page(page))
            result['receipts'] = data
            result['recordsTotal'] = paginator.count
            result['recordsFiltered'] = paginator.count
            result['pages'] = paginator.num_pages
            print(result)
            return JsonResponse(result, safe=False, **response_kwargs)

        else:
            return super(ListView, self).render_to_response(context, **response_kwargs)


class ReceiptView(AdminPermissionRequiredMixin, DetailView):
    permission_required = 'receipts'
    model = Receipt
    template_name = 'admin_receipt/receipt_view.html'


class ReceiptClone(ReceiptUpdate):
    success_message = 'создана'

    def get_form_kwargs(self):
        kwargs = super(ReceiptClone, self).get_form_kwargs()
        receipt_obj = Receipt.objects.get(pk=self.kwargs.get('pk'))
        receipt_obj.number = None
        receipt_obj.pk = None
        kwargs['instance'] = receipt_obj
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ReceiptClone, self).get_context_data(**kwargs)
        if self.request.POST:
            context['receipt_service_formset'] = ReceiptServiceFormSet(self.request.POST, prefix='receipt_service')
        else:
            formset = ReceiptServiceFormSet(prefix='receipt_service',
                                            queryset=ReceiptService.objects.filter(receipt_id=self.kwargs['pk']))
            formset.management_form.initial['INITIAL_FORMS'] = 0
            context['receipt_service_formset'] = formset
        return context


def receipt_delete(request, pk):
    obj_number = None
    try:
        obj_delete = Receipt.objects.get(pk=pk)
        obj_number = obj_delete.number
        if obj_delete.delete():
            success(request, f"Квитанция №{obj_number} успешно удалена")
    except:
        error(request, f"Не удалось удалить квитанцию №{obj_number}")

    return redirect('receipt_list')
