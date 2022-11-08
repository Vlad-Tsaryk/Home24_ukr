from django.urls import path
from .views import PurposeCreate, PurposeList

urlpatterns = [
    path('create/', PurposeCreate.as_view(), name='purpose_create'),
    path('', PurposeList.as_view(), name='purpose_list'),
]
