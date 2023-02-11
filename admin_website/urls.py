from django.urls import path
from .views import MainPageUpdate

urlpatterns = [
    path('main_page/', MainPageUpdate.as_view(), name='website_main_page'),
]