from django.contrib import messages
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from .models import User, Role


class AdminBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if kwargs.get('user_type') == 'admin':
            try:
                admin = User.objects.get(Q(username=username) & ~Q(role__role=Role.RoleName.OWNER))
                if admin.status == admin.StatusName.DISABLED.value:
                    messages.error(request, "Пользователь не активен")
                    return None
                elif admin.check_password(password):
                    return admin
            except User.DoesNotExist:
                messages.error(request, "Пользователь не существует")
                return None


class OwnerBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if kwargs.get('user_type') == 'owner':
            try:
                owner = User.objects.get(Q(username=username) | Q(uid=username), role__role=Role.RoleName.OWNER)
                print(owner)
                if owner.status == owner.StatusName.DISABLED.value:
                    messages.error(request, "Пользователь не активен")
                    return None
                elif owner.check_password(password):
                    return owner
            except User.DoesNotExist:
                messages.error(request, "Пользователь не существует")
                return None
