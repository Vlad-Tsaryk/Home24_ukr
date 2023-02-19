from django.urls import path
from .views import ReceiptList, ReceiptView, ReceiptToPDF

urlpatterns = [
    path('', ReceiptList.as_view(), name='cabinet_receipt_list'),
    path('apartment_id=<apartment_id>', ReceiptList.as_view(), name='cabinet_receipt_list_apartment'),
    path('<pk>', ReceiptView.as_view(), name='cabinet_receipt_view'),
    path('to_<action>/<pk>', ReceiptToPDF.as_view(), name='cabinet_receipt_to_pdf')
]
