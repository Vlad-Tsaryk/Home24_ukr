from django.db.models.functions import Concat
from django.db.models import Value, CharField
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.messages import success, error

from users.mixins import RolePermissionRequiredMixin
from .models import Application
from .forms import ApplicationForm
from admin_apartment.models import Apartment
from users.models import User, Role


# Create your views here.
class ApplicationCreate(RolePermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'applications'
    model = Application
    form_class = ApplicationForm
    template_name = 'admin_application/application_create.html'
    success_url = reverse_lazy('application_list')
    success_message = 'Заявка создана успешно'

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            result = {}
            owner_id = self.request.GET.get('owner_id')
            master_role_id = self.request.GET.get('master_type')
            print(self.request.GET)
            if self.request.GET.get('owner_change'):
                if owner_id:
                    result['apartments'] = list(Apartment.objects.filter(
                        owner_id=owner_id).values('id', 'number', 'house__name'))
                else:
                    result['apartments'] = list(Apartment.objects.all().values('id', 'number', 'house__name'))

            if self.request.GET.get('master_type_change'):
                if master_role_id:
                    result['masters'] = list(User.objects.filter(role=master_role_id).values('id', 'role__role',
                                                                                             'first_name', 'last_name'))
                else:
                    result['masters'] = list(User.objects.filter(
                        role__role__in=[Role.RoleName.PLUMBER, Role.RoleName.ELECTRICIAN]).values('id', 'role__role',
                                                                                                  'first_name',
                                                                                                  'last_name'))

            return JsonResponse(result, safe=False, **response_kwargs)
        else:
            return super(CreateView, self).render_to_response(context, **response_kwargs)


class ApplicationList(RolePermissionRequiredMixin, ListView):
    permission_required = 'applications'
    model = Application
    template_name = 'admin_application/application_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ApplicationList, self).get_context_data(**kwargs)
        context['owner_list'] = User.objects.filter(role__role=Role.RoleName.OWNER)
        context['status_list'] = Application.StatusName.values
        context['master_list'] = User.objects.filter(role__role__in=[Role.RoleName.PLUMBER, Role.RoleName.ELECTRICIAN])
        context['master_types_list'] = Role.objects.filter(role__in=[Role.RoleName.PLUMBER, Role.RoleName.ELECTRICIAN])
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            print(self.request.GET)
            order_by = self.request.GET.get('order_by')
            result = {}
            filter_fields = {
                'status': self.request.GET.get('status'),
                'id__contains': self.request.GET.get('id'),
                'owner_id': self.request.GET.get('owner_id'),
                'apartment_info__contains': self.request.GET.get('apartment'),
                'master__role': self.request.GET.get('master_type'),
                'description__contains': self.request.GET.get('description'),
                'owner__phone__contains': self.request.GET.get('owner_phone'),
                'master_id': self.request.GET.get('master_id'),
                'date__range': self.request.GET.getlist('date_range[]'),
            }

            if self.request.GET.get('master_type_change'):
                if filter_fields['master__role']:
                    result['masters'] = list(
                        User.objects.filter(role=filter_fields['master__role'])
                        .annotate(
                            name=Concat('role__role', Value(' - '), 'first_name', Value(' '), 'last_name', )).values(
                            'id', 'name'))
                else:
                    result['masters'] = list(context['master_list'].annotate(
                            name=Concat('role__role', Value(' - '), 'first_name', Value(' '), 'last_name', )).values(
                            'id', 'name'))
            filter_fields = {k: v for k, v in filter_fields.items() if v}
            filtered_qs = self.get_queryset().annotate(
                apartment_info=Concat(Value('Квартира №'), 'apartment__number', Value(', '),
                                      'apartment__house__name', output_field=CharField())).filter(**filter_fields)
            if order_by:
                filtered_qs = filtered_qs.order_by(order_by)
            filtered_qs = filtered_qs.values('id', 'date', 'time', 'status', 'description', 'apartment_info',
                                             'owner__phone', 'owner__first_name', 'owner__last_name', 'owner_id',
                                             'master__first_name', 'master__last_name', 'master_id', 'apartment_id',
                                             'master__role__role')

            print(filtered_qs)
            result['application'] = list(filtered_qs)
            print(result)
            return JsonResponse(result, safe=False, **response_kwargs)

        else:
            return super(ListView, self).render_to_response(context, **response_kwargs)


class ApplicationView(RolePermissionRequiredMixin, DetailView):
    permission_required = 'applications'
    model = Application
    template_name = 'admin_application/application_view.html'


class ApplicationUpdate(ApplicationCreate, UpdateView):
    template_name = 'admin_application/application_update.html'
    success_message = 'Заявка успешно обновлена'


def application_delete(request, pk):
    obj_id = None
    try:
        obj_delete = Application.objects.get(pk=pk)
        if obj_delete.delete():
            obj_id = pk
    except:
        error(request, f"Не удалось удалить заявку")
    if obj_id:
        success(request, f"Заявка №{obj_id} успешно удалена")
    return redirect('application_list')
