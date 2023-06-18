from django.shortcuts import render
from django.views.generic import DetailView

from admin_website.models import MainPage, ContactPage, ServicePage, AboutPage


# Create your views here.
class MainPageView(DetailView):
    model = MainPage
    template_name = "website/home.html"
    context_object_name = "main_page"

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)
        context["contact_info"] = ContactPage.objects.first()
        return context

    def get_object(self, queryset=None):
        return MainPage.objects.first()


class ContactPageView(DetailView):
    model = ContactPage
    template_name = "website/contact.html"
    context_object_name = "contact_page"

    def get_object(self, queryset=None):
        return ContactPage.objects.first()


class ServicePageView(DetailView):
    model = ServicePage
    template_name = "website/services.html"
    context_object_name = "service_page"

    def get_object(self, queryset=None):
        return ServicePage.objects.first()


class AboutPageView(DetailView):
    model = AboutPage
    template_name = "website/about.html"
    context_object_name = "about_page"

    def get_object(self, queryset=None):
        return AboutPage.objects.first()
