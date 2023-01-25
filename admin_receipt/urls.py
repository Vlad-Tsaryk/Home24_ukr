from django.urls import path
from .views import ReceiptCreate, ReceiptList, ReceiptUpdate, ReceiptView, ReceiptClone
urlpatterns = [
    path('', ReceiptList.as_view(), name='receipt_list'),
    path('create/', ReceiptCreate.as_view(), name='receipt_create'),
    path('update/<pk>', ReceiptUpdate.as_view(), name='receipt_update'),
    path('clone/<pk>', ReceiptClone.as_view(), name='receipt_clone'),
    path('<pk>', ReceiptView.as_view(), name='receipt_view'),


]


