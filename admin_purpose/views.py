from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .models import PaymentDetails


# Create your views here.
class PaymentDetailsUpdate(SuccessMessageMixin, UpdateView):
    model = PaymentDetails
    success_url = reverse_lazy('')
    success_message = "Платежные данные успешно обновлены"
    # form_class =
