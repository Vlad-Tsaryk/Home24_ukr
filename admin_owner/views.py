from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView, FormView

from admin_house.models import House
from admin_personal_account.models import PersonalAccount
from settings import EMAIL_HOST
from users.mixins import AdminPermissionRequiredMixin
from users.models import User, Role
from .forms import OwnerChangeForm, OwnerCreateForm, OwnerInviteForm
from django.db.models.functions import Concat
from django.db.models import Value
from django.contrib import messages


# Create your views here.

class OwnerCreate(AdminPermissionRequiredMixin, CreateView, SuccessMessageMixin):
    permission_required = 'owners'
    model = User
    template_name = 'admin_owner/owner_create.html'
    form_class = OwnerCreateForm
    success_message = "Владелец квартиры успешно создан"
    success_url = reverse_lazy('owner_list')


class OwnerUpdate(AdminPermissionRequiredMixin, UpdateView, SuccessMessageMixin):
    permission_required = 'owners'
    model = User
    template_name = 'admin_owner/owner_update.html'
    form_class = OwnerChangeForm
    success_message = "Владелец квартиры успешно обновлен"
    context_object_name = 'owner'
    success_url = reverse_lazy('owner_list')


class OwnerView(AdminPermissionRequiredMixin, DetailView):
    permission_required = 'owners'
    model = User
    template_name = 'admin_owner/owner_view.html'
    context_object_name = 'owner'


class OwnerDelete(AdminPermissionRequiredMixin, DeleteView):
    permission_required = 'owners'
    model = User
    success_url = reverse_lazy('owner_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        name = self.object.__str__()
        try:
            if self.object.delete():
                messages.success(self.request, f"Пользователь {name} удален успешно")
        except:
            messages.error(request, f"Не удалось удалить пользователя")
        return HttpResponseRedirect(success_url)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class OwnerList(AdminPermissionRequiredMixin, ListView):
    permission_required = 'owners'
    model = User
    template_name = 'admin_owner/owner_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OwnerList, self).get_context_data()
        context['house_list'] = House.objects.all()
        context['status_list'] = User.StatusName.values
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            print(self.request.GET)
            owner_role = Role.objects.get(role=Role.RoleName.OWNER)
            filtered_qs = self.get_queryset() \
                .filter(role=owner_role) \
                .annotate(name=Concat('first_name', Value(' '), 'middle_name', Value(' '), 'last_name'))

            filter_fields = {
                'uid__contains': self.request.GET.get('uid'),
                'name__contains': self.request.GET.get('name'),
                'owner__apartment__number__contains': self.request.GET.get('apartment'),
                'owner__apartment__house': self.request.GET.get('house'),
                'phone__contains': self.request.GET.get('phone'),
                'username__contains': self.request.GET.get('email'),
                'status': self.request.GET.get('status'),
                'date_joined__year': self.request.GET.get('date_year'),
                'date_joined__month': self.request.GET.get('date_month'),
                'date_joined__day': self.request.GET.get('date_day'),
            }
            filter_fields = {k: v for k, v in filter_fields.items() if v}
            filtered_qs = filtered_qs.filter(**filter_fields).order_by('-pk')
            if self.request.GET.get('order_by'):
                filtered_qs = filtered_qs.order_by(self.request.GET.get('order_by'))
            result_list = list(filtered_qs.values('id', 'name', 'phone',
                                                  'username', 'status', 'date_joined', 'uid'))
            print(filtered_qs)
            owner_without_debt = []
            for owner in result_list:
                owner['apartment'] = list(filtered_qs.get(
                    pk=owner['id']).apartment_set.all().values('id', 'number', 'house__name', 'house_id'))
                owner['has_debt'] = PersonalAccount.owner_has_debt(owner['id'])
                if self.request.GET.get('owner_has_debt'):
                    if owner['has_debt']:
                        owner_without_debt.append(owner)

            if self.request.GET.get('owner_has_debt'):
                result_list = owner_without_debt

            start = int(self.request.GET.get('start', 0))
            length = int(self.request.GET.get('length', 10))
            paginator = Paginator(result_list, self.request.GET.get('length', 10))
            page = (start // length) + 1
            data = list(paginator.get_page(page))
            print(data)
            result = {
                'data': data,
                'recordsTotal': paginator.count,
                'recordsFiltered': paginator.count,
                'pages': paginator.num_pages,
            }
            print(result)
            return JsonResponse(result, safe=False, **response_kwargs)
        else:
            return super(ListView, self).render_to_response(context, **response_kwargs)


class OwnerInvite(AdminPermissionRequiredMixin, FormView):
    permission_required = 'owners'
    template_name = 'admin_owner/owner_invite.html'
    form_class = OwnerInviteForm
    success_url = reverse_lazy('owner_invite')

    def form_valid(self, form):
        email = EmailMessage()
        email.from_email = EMAIL_HOST
        email.subject = 'Test'
        email.body = 'Вас приглашают подключиться к системе Demo CRM 24.\n\
        Скачайте приложение:\n\
        Play Market: https://play.google.com/store/apps/details?id=com.avadamedia.program.myhouse24&hl=uk\n\
        App Store: https://itunes.apple.com/us/app/%D0%BC%D0%BE%D0%B9%D0%B4%D0%BE%D0%BC24/id1308075440?l=ru&ls=1&mt=8\n\
        Для дальнейшей информации свяжитесь с администрацией.'
        email.to = [form.cleaned_data.get('email')]
        if email.send():
            messages.success(self.request, 'Email отправлен успешно')
        return super(OwnerInvite, self).form_valid(form)
