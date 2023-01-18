from django.urls import path
from .views import ReceiptCreate
urlpatterns = [
    path('', ReceiptCreate.as_view(), name='receipt_create'),

]
