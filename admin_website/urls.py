from django.urls import path
from .views import MainPageUpdate, ContactPageUpdate, ServicePageUpdate, TariffPageUpdate

urlpatterns = [
    path('main_page/', MainPageUpdate.as_view(), name='website_main_page'),
    path('contact_page/', ContactPageUpdate.as_view(), name='website_contact_page'),
    path('services_page/', ServicePageUpdate.as_view(), name='website_services_page'),
    path('tariffs_page/', TariffPageUpdate.as_view(), name='website_tariffs_page'),
]
