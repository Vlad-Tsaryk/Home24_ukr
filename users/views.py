from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.functions import Concat
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView,DeleteView
from django.http import JsonResponse
from .models import User, Role
from .forms import CustomUserCreationForm, CustomUserUpdateForm, RoleFormSet
from django.db.models import Value
from django.contrib import messages


# Create your views here.

class Users(ListView):
    model = User
    context_object_name = 'user_list'
    template_name = 'users/user_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Users, self).get_context_data(**kwargs)
        context['admin'] = User.objects.get(is_superuser=True)
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            filtered_qs = self.get_queryset().annotate(name=Concat('first_name', Value(' '), 'last_name'))
            filter_fields = {
                'name__contains': self.request.GET.get('name'),
                'role__role': self.request.GET.get('role'),
                'phone__contains': self.request.GET.get('phone'),
                'username__contains': self.request.GET.get('username'),
                'status': self.request.GET.get('status'),
            }
            filter_fields = {k: v for k, v in filter_fields.items() if v}
            filtered_qs = filtered_qs.filter(**filter_fields)
            result_list = list(filtered_qs.values('id', 'name', 'role__role', 'phone', 'username', 'status'))
            return JsonResponse(result_list, safe=False, **response_kwargs)
        else:
            return super(ListView, self).render_to_response(context, **response_kwargs)


class CreateUser(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('user_list')
    success_message = "Пользователь успешно создан"


class UpdateUser(SuccessMessageMixin, UpdateView):
    model = User
    form_class = CustomUserUpdateForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('user_list')
    success_message = "Пользователь успешно изменен"


class ViewUser(DetailView):
    model = User
    template_name = 'users/user_view.html'


def delete_user(request, user_id):
    obj_user = get_object_or_404(User, pk=user_id)
    if not obj_user.is_superuser:
        obj_user.delete()
        messages.success(request, "Пользователь успешно удалён")
    else:
        messages.error(request, "Невозможно удалить администратора")
    return redirect('user_list')


class UpdateRoles(TemplateView):
    template_name = 'users/roles_update.html'
    success_url = reverse_lazy('roles')

    def get_context_data(self, **kwargs):
        context = super(UpdateRoles, self).get_context_data(**kwargs)
        if self.request.POST:
            context['role_formset'] = RoleFormSet(self.request.POST, prefix='role')
        else:
            context['role_formset'] = RoleFormSet(queryset=Role.objects.exclude(role=Role.RoleName.DIRECTOR)
                                                  .exclude(role=Role.RoleName.OWNER),
                                                  prefix='role')
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        role_formset = context['role_formset']
        return self.form_valid(role_formset)

    def form_valid(self, formset):
        print(formset)
        if formset.is_valid():
            print('valid')
            formset.save()
            messages.success(self.request, "Роли успешно изменены")
            return redirect(self.success_url)
        else:
            print(formset.errors)
            print('invalid')