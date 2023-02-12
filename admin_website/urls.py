from django.urls import path
from .views import MainPageUpdate, ContactPageUpdate, ServicePageUpdate, TariffPageUpdate, AboutPageUpdate,\
    GalleryDelete, AdditionalGalleryDelete

urlpatterns = [
    path('main_page/', MainPageUpdate.as_view(), name='website_main_page'),
    path('about_page/', AboutPageUpdate.as_view(), name='website_about_page'),
    path('about_page/delete_gallery_image/<pk>', GalleryDelete.as_view(), name='website_delete_gallery_image'),
    path('about_page/delete_additional_gallery_image/<pk>', AdditionalGalleryDelete.as_view(),
         name='website_delete_additional_gallery_image'),
    path('services_page/', ServicePageUpdate.as_view(), name='website_services_page'),
    path('tariffs_page/', TariffPageUpdate.as_view(), name='website_tariffs_page'),
    path('contact_page/', ContactPageUpdate.as_view(), name='website_contact_page'),
]
