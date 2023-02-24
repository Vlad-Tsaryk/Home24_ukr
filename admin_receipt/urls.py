from django.urls import path, include
from .views import ReceiptCreate, ReceiptList, ReceiptUpdate, ReceiptView, ReceiptClone, receipt_delete
urlpatterns = [
    path('', ReceiptList.as_view(), name='receipt_list'),
    path('apartment_number=<apartment>', ReceiptList.as_view(), name='receipt_list_apartment'),
    path('create/', ReceiptCreate.as_view(), name='receipt_create'),
    path('create/personal_account=<personal_account>', ReceiptCreate.as_view(), name='receipt_create_personal_account'),
    path('update/<pk>', ReceiptUpdate.as_view(), name='receipt_update'),
    path('clone/<pk>', ReceiptClone.as_view(), name='receipt_clone'),
    path('delete/<pk>', receipt_delete, name='receipt_delete'),
    path('<pk>', ReceiptView.as_view(), name='receipt_view'),
    path('template/', include('excel_templates.urls')),
]


