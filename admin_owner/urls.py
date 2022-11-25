from django.urls import path
from .views import OwnerCreate, OwnerUpdate, OwnerList, OwnerView

urlpatterns = [
    path('create/', OwnerCreate.as_view(), name='owner_create'),
    path('update/<pk>', OwnerUpdate.as_view(), name='owner_update'),
    path('<pk>', OwnerView.as_view(), name='owner_view'),
    path('', OwnerList.as_view(), name='owner_list'),
]
