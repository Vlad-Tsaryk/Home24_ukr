from django.shortcuts import render
from django.views.generic import CreateView
from admin_transaction.models import Transaction
from .forms import TransactionForm


# Create your views here.
class TransactionCreate(CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'admin_transaction/transaction_create.html'

    def get_form_kwargs(self):
        kwargs = super(TransactionCreate, self).get_form_kwargs()
        kwargs['transaction_type'] = self.kwargs['transaction_type']
        kwargs['user_id'] = self.request.user.pk
        return kwargs

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            result = {}
            owner_id = self.request.GET.get('owner_id')
            master_role_id = self.request.GET.get('master_type')
            print(self.request.GET)
            if self.request.GET.get('owner_change'):
                if owner_id:
                    result['apartments'] = list(Apartment.objects.filter(
                        owner_id=owner_id).values('id', 'number', 'house__name'))
                else:
                    result['apartments'] = list(Apartment.objects.all().values('id', 'number', 'house__name'))

            if self.request.GET.get('master_type_change'):
                if master_role_id:
                    result['masters'] = list(User.objects.filter(role=master_role_id).values('id', 'role__role',
                                                                                             'first_name', 'last_name'))
                else:
                    result['masters'] = list(User.objects.filter(
                        role__role__in=[Role.RoleName.PLUMBER, Role.RoleName.ELECTRICIAN]).values('id', 'role__role',
                                                                                                  'first_name',
                                                                                                  'last_name'))

            return JsonResponse(result, safe=False, **response_kwargs)
        else:
            return super(CreateView, self).render_to_response(context, **response_kwargs)
