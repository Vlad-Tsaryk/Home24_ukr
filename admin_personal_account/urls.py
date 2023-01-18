from django.urls import path
from .views import PersonalAccountCreate, PersonalAccountList, PersonalAccountUpdate, PersonalAccountView,\
    personal_account_delete

urlpatterns = [
    path('create/', PersonalAccountCreate.as_view(), name='personal_account_create'),
    path('update/<pk>', PersonalAccountUpdate.as_view(), name='personal_account_update'),
    path('delete/<pk>', personal_account_delete, name='personal_account_delete'),
    path('', PersonalAccountList.as_view(), name='personal_account_list'),
    path('<pk>', PersonalAccountView.as_view(), name='personal_account_view')
]
