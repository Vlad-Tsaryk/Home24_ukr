from django.urls import path, re_path

from .views import TransactionCreate, TransactionList

urlpatterns = [
    path('', TransactionList.as_view(), name='transaction_list'),
    path('create/type=<transaction_type>', TransactionCreate.as_view(), name='transaction_create'),
]
