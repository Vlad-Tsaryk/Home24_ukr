from django.urls import path
from .views import MainPageView, ContactPageView, ServicePageView, AboutPageView

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('contact', ContactPageView.as_view(), name='contact_page'),
    path('services', ServicePageView.as_view(), name='service_page'),
    path('about', AboutPageView.as_view(), name='about_page'),
]
