from django.shortcuts import render
from django.views.generic import CreateView

from .models import Application
from .forms import ApplicationForm


# Create your views here.
class ApplicationCreate(CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'admin_application/application_create.html'
