from django.urls import path
from .views import (
    TransactionCreate,
    TransactionList,
    TransactionView,
    TransactionUpdate,
    TransactionClone,
    TransactionDelete,
    TransactionToExcel,
)

urlpatterns = [
    path("", TransactionList.as_view(), name="transaction_list"),
    path(
        "personal_account=<personal_account>",
        TransactionList.as_view(),
        name="transaction_list_personal_account",
    ),
    path("<pk>", TransactionView.as_view(), name="transaction_view"),
    path("update/<pk>", TransactionUpdate.as_view(), name="transaction_update"),
    path("clone/<pk>", TransactionClone.as_view(), name="transaction_clone"),
    path(
        "create/type=<transaction_type>",
        TransactionCreate.as_view(),
        name="transaction_create",
    ),
    path(
        "create/type=<transaction_type>/personal_account_id=<personal_account_id>",
        TransactionCreate.as_view(),
        name="transaction_create_personal_account",
    ),
    path("delete/<pk>", TransactionDelete.as_view(), name="transaction_delete"),
    path("to_excel/<pk>", TransactionToExcel.as_view(), name="transaction_to_excel"),
]
