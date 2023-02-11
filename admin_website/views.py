from django.shortcuts import render
from django.views.generic import UpdateView

from admin_website.forms import MainPageForm
from admin_website.models import MainPage


# Create your views here.
class MainPageUpdate(UpdateView):
    model = MainPage
    form_class = MainPageForm
    context_object_name = 'main_page'
    template_name = 'admin_website/main_page.html'

    def get_object(self, queryset=None):
        return MainPage.objects.first()
