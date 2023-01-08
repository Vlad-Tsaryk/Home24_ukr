from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView, ListView

from .models import Application
from .forms import ApplicationForm
from admin_apartment.models import Apartment
from users.models import User, Role


# Create your views here.
class ApplicationCreate(CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'admin_application/application_create.html'

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            result = {}
            owner_id = self.request.GET.get('owner_id')
            master_role_id = self.request.GET.get('master_type')
            # apartment_id = self.request.GET.get('apartment_id')
            print(self.request.GET)
            # if apartment_id:
            #     result['apartments'] = list(User.objects.get(
            #         apartment=apartment_id).values('id'))
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


class ApplicationList(ListView):
    model = Application
    template_name = 'admin_application/application_list.html'
