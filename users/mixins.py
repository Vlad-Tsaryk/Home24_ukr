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
        try:
            if self.request.user.role.role == Role.RoleName.OWNER:
                if self.request.COOKIES.get('admin_session_key') != 'None':
                    try:
                        session_object_model = Session.objects.get(
                            session_key=self.request.COOKIES.get(f'admin_session_key'))
                        if session_object_model.get_decoded():
                            session_store = SessionStore(session_object_model.session_key)
                            user_id = session_object_model.get_decoded().get('_auth_user_id')
                            if user_id:
                                self.request.session = session_store
                                self.request.user = User.objects.get(pk=user_id)
                                return all(getattr(self.request.user.role, f'{perm}') for perm in perms)
                    except (Session.DoesNotExist, KeyError, User.DoesNotExist):
                        self.request.session = SessionStore(None)

                return redirect(self.login_url)
            else:
                return all(getattr(self.request.user.role, f'{perm}') for perm in perms)
        except:
            return redirect(self.login_url)

    def dispatch(self, request, *args, **kwargs):
        has_permission = self.has_permission()
        if has_permission == False:
            return self.handle_no_permission()
        elif has_permission == True:
            return super().dispatch(request, *args, **kwargs)
        else:
            return has_permission


class OwnerPermissionRequiredMixin(LoginRequiredMixin, PermissionRequiredMixin):
    login_url = reverse_lazy('cabinet_login')

    def has_permission(self):
        try:
            if self.request.user.role.role != Role.RoleName.OWNER:
                if self.request.COOKIES.get('owner_session_key') != 'None':
                    try:
                        session_object_model = Session.objects.get(
                            session_key=self.request.COOKIES.get(f'owner_session_key'))
                        if session_object_model.get_decoded():
                            session_store = SessionStore(session_object_model.session_key)
                            user_id = session_object_model.get_decoded().get('_auth_user_id')
                            if user_id:
                                self.request.session = session_store
                                self.request.user = User.objects.get(pk=user_id)
                                return True
                    except (Session.DoesNotExist, KeyError, User.DoesNotExist):
                        self.request.session = SessionStore(None)
                return redirect(self.login_url)
            else:
                return True
        except:
            return redirect(self.login_url)

    def dispatch(self, request, *args, **kwargs):
        has_permission = self.has_permission()
        if has_permission:
            return super().dispatch(request, *args, **kwargs)
        return has_permission
