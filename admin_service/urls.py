from django.urls import path
from .views import ServiceEdit

urlpatterns = [
    path('', ServiceEdit.as_view(), name='service'),
]
