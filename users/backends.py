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
                    messages.error(request, "Користувач не aктивний")
                    return None
                elif admin.check_password(password):
                    return admin
                else:
                    messages.error(request, "Пароль введений неправильно")
            except User.DoesNotExist:
                messages.error(request, "Користувач не існує")
                return None


class OwnerBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if kwargs.get('user_type') == 'owner':
            try:
                owner = User.objects.get(Q(username=username) | Q(uid=username), role__role=Role.RoleName.OWNER)
                print('Password', owner.check_password(password))
                if owner.status == owner.StatusName.DISABLED.value:
                    messages.error(request, "Користувач не активний")
                    return None
                elif owner.check_password(password):
                    return owner
                else:
                    messages.error(request, "Пароль введений неправильно")
            except User.DoesNotExist:
                messages.error(request, "Користувача не існує")
                return None
