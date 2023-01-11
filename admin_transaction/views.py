from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from admin_transaction.models import Transaction
from .forms import TransactionForm
from admin_personal_account.models import PersonalAccount
from users.models import User, Role
from admin_purpose.models import Purpose


# Create your views here.
class TransactionCreate(CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'admin_transaction/transaction_create.html'
    success_url = reverse_lazy('transaction_list')

    def get_form_kwargs(self):
        kwargs = super(TransactionCreate, self).get_form_kwargs()
        kwargs['transaction_type'] = self.kwargs['transaction_type']
        kwargs['user_id'] = self.request.user.pk
        return kwargs

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            result = {}
            owner_id = self.request.GET.get('owner_id')
            personal_account_id = self.request.GET.get('personal_account')
            print(self.request.GET)
            if self.request.GET.get('owner_change'):
                if owner_id:
                    result['personal_accounts'] = list(PersonalAccount.objects.filter(
                        apartment__owner=owner_id).values('id', 'number'))
                else:
                    result['personal_accounts'] = list(PersonalAccount.objects.all().values('id', 'number'))

            if self.request.GET.get('personal_account_change'):
                if personal_account_id:
                    result['owner_id'] = str(PersonalAccount.objects.get(
                        pk=personal_account_id).apartment.owner_id)
            print(result)
            return JsonResponse(result, safe=False, **response_kwargs)
        else:
            return super(CreateView, self).render_to_response(context, **response_kwargs)


class TransactionList(ListView):
    model = Transaction
    template_name = 'admin_transaction/transaction_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TransactionList, self).get_context_data(**kwargs)
        context['owner_list'] = User.objects.filter(role__role=Role.RoleName.OWNER)
        context['purpose_list'] = Purpose.objects.all()
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            print(self.request.GET)
            order_by = self.request.GET.get('order_by')
            result = {}
            filter_fields = {
                'status': self.request.GET.get('status'),
                'id__contains': self.request.GET.get('id'),
                'owner_id': self.request.GET.get('owner_id'),
                'apartment_info__contains': self.request.GET.get('apartment'),
                'master__role': self.request.GET.get('master_type'),
                'description__contains': self.request.GET.get('description'),
                'owner__phone__contains': self.request.GET.get('owner_phone'),
                'master_id': self.request.GET.get('master_id'),
                'date__range': self.request.GET.getlist('date_range[]'),
            }

            # if self.request.GET.get('master_type_change'):
            #     if filter_fields['master__role']:
            #         result['masters'] = list(
            #             User.objects.filter(role=filter_fields['master__role'])
            #             .annotate(
            #                 name=Concat('role__role', Value(' - '), 'first_name', Value(' '), 'last_name', )).values(
            #                 'id', 'name'))
            #     else:
            #         result['masters'] = list(context['master_list'].annotate(
            #                 name=Concat('role__role', Value(' - '), 'first_name', Value(' '), 'last_name', )).values(
            #                 'id', 'name'))
            filter_fields = {k: v for k, v in filter_fields.items() if v}
            filtered_qs = self.get_queryset().filter(**filter_fields)
            if order_by:
                filtered_qs = filtered_qs.order_by(order_by)
            filtered_qs = filtered_qs.values('id', 'date', 'is_complete', 'type', 'number', 'owner__first_name',
                                             'owner__last_name', 'owner_id', 'personal_account__number', 'sum',
                                             'purpose__name', 'owner__middle_name')

            print(filtered_qs)
            result['transaction'] = list(filtered_qs)
            print(result)
            return JsonResponse(result, safe=False, **response_kwargs)

        else:
            return super(ListView, self).render_to_response(context, **response_kwargs)


class TransactionView(DetailView):
    model = Transaction
    template_name = 'admin_transaction/transaction_view.html'
