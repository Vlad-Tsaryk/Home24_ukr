from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, ListView

from users.mixins import AdminPermissionRequiredMixin
from .models import PaymentDetails, Purpose
from .forms import PaymentDetailsForm, PurposeForm
from django.contrib import messages


# Create your views here.
class PaymentDetailsUpdate(
    AdminPermissionRequiredMixin, SuccessMessageMixin, UpdateView
):
    permission_required = "payment_details"
    model = PaymentDetails
    success_url = reverse_lazy("payment_details_update")
    success_message = "Платіжні дані успішно оновлені"
    form_class = PaymentDetailsForm
    template_name = "admin_purpose/payment_details.html"

    def get_object(self, **kwargs):
        return PaymentDetails.objects.first()


class PurposeCreate(AdminPermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = "payment_details"
    model = Purpose
    success_url = reverse_lazy("purpose_list")
    success_message = "Стаття успішно додана"
    form_class = PurposeForm
    template_name = "admin_purpose/purpose_create.html"


class PurposeList(AdminPermissionRequiredMixin, ListView):
    permission_required = "payment_details"
    model = Purpose
    template_name = "admin_purpose/purpose_list.html"


class PurposeUpdate(AdminPermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = "payment_details"
    model = Purpose
    form_class = PurposeForm
    success_url = reverse_lazy("purpose_list")
    success_message = "Стаття успішно змінено"
    template_name = "admin_purpose/purpose_update.html"


def purpose_delete(request, pk):
    obj_purpose = get_object_or_404(Purpose, pk=pk)
    name = obj_purpose.name
    obj_purpose.delete()
    messages.success(request, f"Стаття {name} успішно видалена")
    return redirect("purpose_list")
