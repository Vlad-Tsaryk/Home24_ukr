from django.urls import path
from .views import CabinetApplicationList, CabinetApplicationCreate, CabinetApplicationDelete
urlpatterns = [
    path('', CabinetApplicationList.as_view(), name='cabinet_application_list'),
    path('create/', CabinetApplicationCreate.as_view(), name='cabinet_application_create'),
    path('delete/<pk>', CabinetApplicationDelete.as_view(), name='cabinet_application_delete'),

]
