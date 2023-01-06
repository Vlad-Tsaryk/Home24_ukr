from django.urls import path
from .views import ApplicationCreate

urlpatterns = [
    path('create/', ApplicationCreate.as_view(), name='application_create'),
]
