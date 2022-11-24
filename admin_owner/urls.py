from django.urls import path
from .views import OwnerCreate, OwnerUpdate

urlpatterns = [
    path('create/', OwnerCreate.as_view(), name='owner_create'),
    path('update/<pk>', OwnerUpdate.as_view(), name='owner_update'),
]
