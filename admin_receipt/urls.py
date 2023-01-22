from django.urls import path
from .views import ReceiptCreate, ReceiptList
urlpatterns = [
    path('', ReceiptList.as_view(), name='receipt_list'),
    path('create/', ReceiptCreate.as_view(), name='receipt_create'),


]


