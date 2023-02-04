from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin


class RolePermissionRequiredMixin(LoginRequiredMixin, PermissionRequiredMixin):

    def has_permission(self):
        perms = self.get_permission_required()
        return all(getattr(self.request.user.role, f'{perm}') for perm in perms)
