from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views.generic import TemplateView

from users.mixins import RolePermissionRequiredMixin


# Create your views here.

class StatisticView(RolePermissionRequiredMixin, TemplateView):
    permission_required = 'statistics'
    template_name = 'admin_panel/statistic.html'


def error_404(request, exception):
    return render(request, 'admin_panel/error_404.html')


def error_403(request, exception):
    return render(request, 'admin_panel/error_403.html')




class AdminLoginView(TemplateView):
    template_name = 'admin_panel/login_page.html'
    pass
