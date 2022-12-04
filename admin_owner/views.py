from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from users.models import User, Role
from .forms import OwnerChangeForm, OwnerCreateForm
from django.db.models.functions import Concat
from django.db.models import Value
from django.contrib import messages


# Create your views here.

class OwnerCreate(CreateView, SuccessMessageMixin):
    model = User
    template_name = 'admin_owner/owner_create.html'
    form_class = OwnerCreateForm
    success_message = "Владелец квартиры успешно создан"
    success_url = reverse_lazy('owner_list')


class OwnerUpdate(UpdateView, SuccessMessageMixin):
    model = User
    template_name = 'admin_owner/owner_update.html'
    form_class = OwnerChangeForm
    success_message = "Владелец квартиры успешно обновлен"
    context_object_name = 'owner'
    success_url = reverse_lazy('owner_list')


class OwnerView(DetailView):
    model = User
    template_name = 'admin_owner/owner_view.html'
    context_object_name = 'owner'


def owner_delete(request, pk):
    user_name = None
    try:
        obj_delete = User.objects.get(pk=pk)
        name = obj_delete.__str__()
        if obj_delete.delete():
            user_name = name
    except:
        messages.error(request, f"Не удалось удалить пользователя")
    if user_name:
        messages.success(request, f"Пользователь {user_name} удален успешно")
    return redirect('owner_list')


class OwnerList(ListView):
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
                                                  'username', 'status', 'date_joined'))
            for owner in result_list:
                owner['apartment'] = list(filtered_qs.get(
                    pk=owner['id']).apartment_set.all().values('id', 'number', 'house__name', 'house_id'))
            print(result_list)
            return JsonResponse(result_list, safe=False, **response_kwargs)
        else:
            return super(ListView, self).render_to_response(context, **response_kwargs)
