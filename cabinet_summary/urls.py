from django.urls import path
from .views import ApartmentSummary

urlpatterns = [
    path('apartment_id=<pk>', ApartmentSummary.as_view(), name='cabinet_apartment_summary'),
]
