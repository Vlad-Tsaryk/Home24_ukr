from django.urls import path
from .views import TransactionCreate, TransactionList, TransactionView, TransactionUpdate, TransactionClone,\
    transaction_delete

urlpatterns = [
    path('', TransactionList.as_view(), name='transaction_list'),
    path('<pk>', TransactionView.as_view(), name='transaction_view'),
    path('update/<pk>', TransactionUpdate.as_view(), name='transaction_update'),
    path('clone/<pk>', TransactionClone.as_view(), name='transaction_clone'),
    path('create/type=<transaction_type>', TransactionCreate.as_view(), name='transaction_create'),
    path('delete/<pk>', transaction_delete, name='transaction_delete'),
]
