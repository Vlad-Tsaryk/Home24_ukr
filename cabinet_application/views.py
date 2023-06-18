from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView

from admin_application.models import Application
from cabinet_application.forms import CabinetApplicationForm
from users.mixins import OwnerPermissionRequiredMixin


# Create your views here.
class CabinetApplicationList(OwnerPermissionRequiredMixin, ListView):
    model = Application
    template_name = "cabinet_application/application_list.html"

    def get_queryset(self):
        return Application.objects.filter(owner=self.request.user)

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            data = self.get_queryset().values(
                "id", "date", "time", "status", "description", "master_type"
            )
            start = int(self.request.GET.get("start", 0))
            length = int(self.request.GET.get("length", 10))
            paginator = Paginator(data, self.request.GET.get("length", 10))
            page = (start // length) + 1
            data = list(paginator.get_page(page))
            print(data)
            result = {
                "application": data,
                "recordsTotal": paginator.count,
                "recordsFiltered": paginator.count,
                "pages": paginator.num_pages,
            }
            print(result)
            return JsonResponse(result, safe=False, **response_kwargs)
        else:
            return super(ListView, self).render_to_response(context, **response_kwargs)


class CabinetApplicationCreate(OwnerPermissionRequiredMixin, CreateView):
    model = Application
    form_class = CabinetApplicationForm
    template_name = "cabinet_application/application_create.html"
    success_url = reverse_lazy("cabinet_application_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["owner_id"] = self.request.user
        return kwargs

    def form_valid(self, form):
        application = form.save(commit=False)
        application.owner = self.request.user
        application.status = Application.StatusName.NEW
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class CabinetApplicationDelete(OwnerPermissionRequiredMixin, DeleteView):
    model = Application
    success_url = reverse_lazy("cabinet_application_list")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.status != Application.StatusName.NEW:
            messages.error(
                self.request, "Неможливо видалити заявку, оскільки вона вже оброблена"
            )
        else:
            application_number = self.object.pk
            if self.object.delete():
                messages.success(
                    self.request, f"Заявка №{application_number} успішно видалена"
                )
        return HttpResponseRedirect(self.get_success_url())
