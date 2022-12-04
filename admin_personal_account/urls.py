from django.urls import path
from .views import PersonalAccountCreate, PersonalAccountList

urlpatterns = [
    path('create/', PersonalAccountCreate.as_view(), name='personal_account_create'),
    path('', PersonalAccountList.as_view(), name='personal_account_list')
]
