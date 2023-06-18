from django.urls import path
from .views import ApartmentSummary, ApartmentSummaryRedirect

urlpatterns = [
    path(
        "apartment_id=<pk>",
        ApartmentSummary.as_view(),
        name="cabinet_apartment_summary",
    ),
    path("", ApartmentSummaryRedirect.as_view(), name="cabinet"),
]
