from django.contrib.auth import authenticate, login, logout
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sessions.backends.db import SessionStore
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.db.models.functions import Concat
from django.db.models import Value, ProtectedError
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView, DeleteView, FormView
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic.detail import SingleObjectMixin

from home24 import settings
from .mixins import AdminPermissionRequiredMixin
from .models import User, Role
from .forms import CustomUserCreationForm, CustomUserUpdateForm, RoleFormSet, AdminLoginForm, CabinetLoginForm
from django.contrib import messages


# Create your views here.

class Users(AdminPermissionRequiredMixin, ListView):
    permission_required = 'users'
    model = User
    context_object_name = 'user_list'
    template_name = 'users/user_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Users, self).get_context_data(**kwargs)
        context['admin'] = User.objects.get(is_superuser=True)
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            owner_role = Role.objects.get(role=Role.RoleName.OWNER)
            filtered_qs = self.get_queryset().exclude(role=owner_role) \
                .annotate(name=Concat('first_name', Value(' '), 'last_name'))
            filter_fields = {
                'name__contains': self.request.GET.get('name'),
                'role__role': self.request.GET.get('role'),
                'phone__contains': self.request.GET.get('phone'),
                'username__contains': self.request.GET.get('username'),
                'status': self.request.GET.get('status'),
            }
            filter_fields = {k: v for k, v in filter_fields.items() if v}
            filtered_qs = filtered_qs.filter(**filter_fields)
            filtered_qs = filtered_qs.values('id', 'name', 'role__role', 'phone', 'username', 'status')
            start = int(self.request.GET.get('start', 0))
            length = int(self.request.GET.get('length', 10))
            paginator = Paginator(filtered_qs, self.request.GET.get('length', 10))
            page = (start // length) + 1
            data = list(paginator.get_page(page))
            result = {
                'data': data,
                'recordsTotal': paginator.count,
                'recordsFiltered': paginator.count,
                'pages': paginator.num_pages,
            }
            return JsonResponse(result, safe=False, **response_kwargs)
        else:
            return super(ListView, self).render_to_response(context, **response_kwargs)


class InviteUser(View, SingleObjectMixin):
    model = User

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        email = EmailMessage()
        email.from_email = settings.EMAIL_HOST
        email.subject = 'Приглашение в Home 24'
        email.body = f'Вас приглашают подключиться к системе Home 24 с уровнем доступа: {user.role.role}.\nВаш логин:' \
                     f'{user.username} Чтобы узнать пароль свяжитесь с администрацией.\nСсылка для входа: ' \
                     f'http://164.92.196.234/admin/site/login'
        email.to = [user.username]
        if email.send():
            messages.success(self.request, f'Приглашение для пользователя <b>{user.username}</b> отправлено')
        return redirect('user_list')


class CreateUser(AdminPermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'users'
    form_class = CustomUserCreationForm
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('user_list')
    success_message = "Пользователь успешно создан"


class UpdateUser(AdminPermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'users'
    model = User
    context_object_name = 'obj_user'
    form_class = CustomUserUpdateForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('user_list')
    success_message = "Пользователь успешно изменен"


class ViewUser(AdminPermissionRequiredMixin, DetailView):
    permission_required = 'users'
    model = User
    context_object_name = 'obj_user'
    template_name = 'users/user_view.html'


class DeleteUser(AdminPermissionRequiredMixin, DeleteView):
    permission_required = 'users'
    model = User
    success_url = reverse_lazy('user_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        if self.object.is_superuser:
            messages.error(request, "Невозможно удалить администратора")
        else:
            try:
                if self.object.delete():
                    messages.success(request, 'Пользователь успешно удален')
            except ProtectedError as e:
                protected_object = list(e.protected_objects)[0]

                model_name = protected_object._meta.model_name
                if model_name == 'application':
                    messages.error(request, 'У мастера есть заявки')
                else:
                    messages.error(request, 'Пользователь является менеджером в транзакциях')
        return HttpResponseRedirect(success_url)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class UpdateRoles(AdminPermissionRequiredMixin, TemplateView):
    permission_required = 'roles'
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


class CustomLoginView(FormView):
    user_type = ''

    def authenticated_check(self):
        if self.request.COOKIES.get(f'{self.user_type}_session_key'):
            if self.request.COOKIES.get(f'{self.user_type}_session_key') != 'None':
                return True
        return False

    def get(self, request, *args, **kwargs):
        if self.request.session:
            self.request.session = SessionStore(None)
        if self.authenticated_check():
            return redirect(self.success_url)
        return super().get(self, request, *args, **kwargs)

    def form_valid(self, form):
        user = authenticate(self.request, username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'], user_type=self.user_type)
        if user is not None:
            login(self.request, user)
            if not form.cleaned_data['remember_me']:
                self.request.session.set_expiry(0)

            response = redirect(self.success_url)
            response.set_cookie(f'{self.user_type}_session_key', self.request.session.session_key,
                                max_age=self.request.session.get_expiry_age())
            return response
        else:
            return super(CustomLoginView, self).get(self.request)


class AdminLoginView(CustomLoginView):
    template_name = 'admin_panel/login_page.html'
    form_class = AdminLoginForm
    success_url = reverse_lazy('statistic')
    user_type = 'admin'


class CabinetLoginView(CustomLoginView):
    template_name = 'cabinet/login_page.html'
    form_class = CabinetLoginForm
    success_url = reverse_lazy('cabinet')
    user_type = 'owner'

    # def get(self, request, *args, **kwargs):
    #     # if self.request.user.is_authenticated:
    #     #     return redirect('ca')
    #     return super(LoginView).get(self, request, *args, **kwargs)


class LogoutView(View):
    success_url = ''
    user_type = ''

    def get(self, request, *args, **kwargs):
        print(self.request.user)
        if self.request.user.is_authenticated:
            logout(request)
        response = HttpResponseRedirect(self.success_url)
        response.set_cookie(f'{self.user_type}_session_key', None)
        return response


class AdminLogoutView(LogoutView):
    success_url = reverse_lazy('admin-panel-login')
    user_type = 'admin'


class CabinetLogoutView(LogoutView):
    success_url = reverse_lazy('cabinet_login')
    user_type = 'owner'
