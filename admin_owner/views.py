from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMessage
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView, FormView

from admin_personal_account.models import PersonalAccount
from settings import EMAIL_HOST
from users.mixins import RolePermissionRequiredMixin
from users.models import User, Role
from .forms import OwnerChangeForm, OwnerCreateForm, OwnerInviteForm
from django.db.models.functions import Concat
from django.db.models import Value
from django.contrib import messages


# Create your views here.

class OwnerCreate(RolePermissionRequiredMixin, CreateView, SuccessMessageMixin):
    permission_required = 'owners'
    model = User
    template_name = 'admin_owner/owner_create.html'
    form_class = OwnerCreateForm
    success_message = "Владелец квартиры успешно создан"
    success_url = reverse_lazy('owner_list')


class OwnerUpdate(RolePermissionRequiredMixin, UpdateView, SuccessMessageMixin):
    permission_required = 'owners'
    model = User
    template_name = 'admin_owner/owner_update.html'
    form_class = OwnerChangeForm
    success_message = "Владелец квартиры успешно обновлен"
    context_object_name = 'owner'
    success_url = reverse_lazy('owner_list')


class OwnerView(RolePermissionRequiredMixin, DetailView):
    permission_required = 'owners'
    model = User
    template_name = 'admin_owner/owner_view.html'
    context_object_name = 'owner'


class OwnerDelete(RolePermissionRequiredMixin, DeleteView):
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


class OwnerList(RolePermissionRequiredMixin, ListView):
    permission_required = 'owners'
    model = User
    template_name = 'admin_owner/owner_list.html'

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            print(self.request.GET)
            owner_role = Role.objects.get(role=Role.RoleName.OWNER)
            filtered_qs = self.get_queryset().filter(role=owner_role).annotate(name=Concat('first_name',
                                                                                           Value(' '), 'middle_name',
                                                                                           Value(' '), 'last_name'))
            filter_fields = {
                'name__contains': self.request.GET.get('name'),
                'role__role': self.request.GET.get('role'),
                'phone__contains': self.request.GET.get('phone'),
                'username__contains': self.request.GET.get('username'),
                'status': self.request.GET.get('status'),
            }
            filter_fields = {k: v for k, v in filter_fields.items() if v}
            filtered_qs = filtered_qs.filter(**filter_fields)
            if self.request.GET.get('order_by'):
                filtered_qs = filtered_qs.order_by(self.request.GET.get('order_by'))
            result_list = list(filtered_qs.values('id', 'name', 'phone',
                                                  'username', 'status', 'date_joined', 'uid'))
            for owner in result_list:
                owner['apartment'] = list(filtered_qs.get(
                    pk=owner['id']).apartment_set.all().values('id', 'number', 'house__name', 'house_id'))
                owner['has_debt'] = PersonalAccount.owner_has_debt(owner['id'])
            print(result_list)
            return JsonResponse(result_list, safe=False, **response_kwargs)
        else:
            return super(ListView, self).render_to_response(context, **response_kwargs)


class OwnerInvite(RolePermissionRequiredMixin, FormView):
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
