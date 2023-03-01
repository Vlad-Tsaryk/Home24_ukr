from django.contrib.auth import login
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.shortcuts import redirect
from django.urls import reverse_lazy

from users.models import Role, User


class AdminPermissionRequiredMixin(LoginRequiredMixin, PermissionRequiredMixin):
    login_url = reverse_lazy('admin-panel-login')

    def has_permission(self):
        perms = self.get_permission_required()
        if self.request.user.is_anonymous or self.request.user.role.role == Role.RoleName.OWNER:
            admin_session_key = self.request.COOKIES.get('admin_session_key')
            if admin_session_key != 'None':
                try:
                    Session.objects.get(session_key=admin_session_key)
                    session = Session.objects.get(session_key=admin_session_key)
                    self.request.session = SessionStore(session.session_key)
                    self.request.session['sessionid'] = admin_session_key
                    user_id = session.get_decoded().get('_auth_user_id')
                    self.request.user = User.objects.get(pk=user_id)
                    return True
                except (Session.DoesNotExist, KeyError, User.DoesNotExist):
                    return 'redirect'
            return 'redirect'
        else:
            return all(getattr(self.request.user.role, f'{perm}') for perm in perms)

    def dispatch(self, request, *args, **kwargs):
        has_permission = self.has_permission()
        if has_permission == 'redirect':
            return redirect(self.login_url)
        elif has_permission:
            return super().dispatch(request, *args, **kwargs)
        else:
            return self.handle_no_permission()


class OwnerPermissionRequiredMixin(LoginRequiredMixin, PermissionRequiredMixin):
    login_url = reverse_lazy('cabinet_login')

    def has_permission(self):
        owner_session_key = self.request.COOKIES.get('owner_session_key')
        if self.request.user.is_anonymous or self.request.user.role.role != Role.RoleName.OWNER:
            if owner_session_key != 'None':
                try:
                    session_store = SessionStore(owner_session_key)
                    session_object_model = Session.objects.get(session_key=owner_session_key)
                    if session_object_model.get_decoded():
                        user_id = session_object_model.get_decoded().get('_auth_user_id')
                        if user_id:
                            self.request.session = session_store
                            self.request.session['sessionid'] = owner_session_key
                            self.request.user = User.objects.get(pk=user_id)
                            return True
                except (Session.DoesNotExist, KeyError, User.DoesNotExist):
                    return False
            else:
                return False
        else:
            return True

    def dispatch(self, request, *args, **kwargs):
        has_permission = self.has_permission()
        if has_permission:
            return super().dispatch(request, *args, **kwargs)
        return redirect(self.login_url)
