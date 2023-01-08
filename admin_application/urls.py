from django.urls import path
from .views import ApplicationCreate, ApplicationList

urlpatterns = [
    path('', ApplicationList.as_view(), name='application_list'),
    path('create/', ApplicationCreate.as_view(), name='application_create'),

]
