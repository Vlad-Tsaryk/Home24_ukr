from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from admin_transaction.models import Transaction
from users.mixins import RolePermissionRequiredMixin
from .forms import TransactionForm
from admin_personal_account.models import PersonalAccount
from users.models import User, Role
from admin_purpose.models import Purpose
from django.contrib.messages import success, error


# Create your views here.
class TransactionCreate(RolePermissionRequiredMixin, CreateView):
    permission_required = 'transactions'
    model = Transaction
    form_class = TransactionForm
    template_name = 'admin_transaction/transaction_create.html'
    success_url = reverse_lazy('transaction_list')

    def get_form_kwargs(self):
        kwargs = super(TransactionCreate, self).get_form_kwargs()
        kwargs['transaction_type'] = self.kwargs.get('transaction_type')
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


class TransactionUpdate(TransactionCreate, UpdateView):
    template_name = 'admin_transaction/transaction_update.html'
    model = Transaction
    form_class = TransactionForm
    success_url = reverse_lazy('transaction_list')


class TransactionClone(TransactionUpdate):
    template_name = 'admin_transaction/transaction_update.html'

    def get_form_kwargs(self):
        kwargs = super(TransactionClone, self).get_form_kwargs()
        transaction_obj = Transaction.objects.get(pk=self.kwargs['pk'])
        if transaction_obj:
            transaction_obj.pk = None
            transaction_obj.number = None
            kwargs['instance'] = transaction_obj
        return kwargs


class TransactionList(RolePermissionRequiredMixin, ListView):
    permission_required = 'transactions'
    model = Transaction
    template_name = 'admin_transaction/transaction_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TransactionList, self).get_context_data(**kwargs)
        context['owner_list'] = User.objects.filter(role__role=Role.RoleName.OWNER)
        context['account_total_debt'] = PersonalAccount.total_debt()
        context['account_total_balance'] = PersonalAccount.total_balance()
        context['transactions_total_balance'] = Transaction.total_balance()
        context['purpose_list'] = Purpose.objects.all()
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            print(self.request.GET)
            order_by = self.request.GET.get('order_by')
            result = {}
            filter_fields = {
                'status': self.request.GET.get('status'),
                'number__contains': self.request.GET.get('number'),
                'owner_id': self.request.GET.get('owner'),
                'type': self.request.GET.get('purpose_type'),
                'personal_account__number__contains': self.request.GET.get('personal_account__number'),
                'purpose': self.request.GET.get('purpose'),
                'is_complete': self.request.GET.get('is_complete'),
                'date__range': self.request.GET.getlist('date_range[]'),
            }
            # if self.request.GET.get('purpose_type_change'):
            #     if filter_fields['type']:
            #         result['purposes'] = list(
            #             context['purpose_list'].filter(transaction_type=filter_fields['type']).values('name'))
            #     else:
            #         result['purposes'] = list(context['purpose_list'].values('name'))
            filter_fields = {k: v for k, v in filter_fields.items() if v}
            filtered_qs = self.get_queryset().filter(**filter_fields)
            if order_by:
                filtered_qs = filtered_qs.order_by(order_by)
            result['income'] = '%.2f' % self.model.count_income(filtered_qs)
            result['outcome'] = '%.2f' % self.model.count_outcome(filtered_qs)
            filtered_qs = filtered_qs.values('id', 'date', 'is_complete', 'type', 'number', 'owner__first_name',
                                             'owner__last_name', 'owner_id', 'personal_account__number', 'sum',
                                             'purpose__name', 'owner__middle_name')

            print(filtered_qs)
            result['transaction'] = list(filtered_qs)
            print(result)
            return JsonResponse(result, safe=False, **response_kwargs)

        else:
            return super(ListView, self).render_to_response(context, **response_kwargs)


class TransactionView(RolePermissionRequiredMixin, DetailView):
    permission_required = 'transactions'
    model = Transaction
    template_name = 'admin_transaction/transaction_view.html'


def transaction_delete(request, pk):
    obj_number = None
    try:
        obj_delete = Transaction.objects.get(pk=pk)
        number = obj_delete.number
        if obj_delete.delete():
            obj_number = number
    except:
        error(request, f"Не удалось удалить ведомость")
    if obj_number:
        success(request, f"Ведомость №{obj_number} успешно удалена")
    return redirect('transaction_list')
