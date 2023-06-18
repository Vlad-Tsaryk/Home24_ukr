from django.urls import path
from .views import (
    MeterCreate,
    MeterList,
    MeterClone,
    MeterNewValue,
    MeterViewList,
    MeterUpdate,
    MeterView,
    meter_delete,
)

urlpatterns = [
    path("create/", MeterCreate.as_view(), name="meter-create"),
    path("update/<pk>", MeterUpdate.as_view(), name="meter-update"),
    path("delete/<pk>", meter_delete, name="meter-delete"),
    path("create/clone_id=<pk>", MeterClone.as_view(), name="meter-clone"),
    path("<pk>", MeterView.as_view(), name="meter-view"),
    path(
        "create/apartment=<apartment_id>",
        MeterNewValue.as_view(),
        name="meter-new-value",
    ),
    path(
        "create/apartment_id=<apartment_id>_service=<service_id>",
        MeterNewValue.as_view(),
        name="meter-new-value-serv",
    ),
    path(
        "meter_list/apartment=<apartment_id>_service=<service_id>",
        MeterViewList.as_view(),
        name="meter-view-list-serv",
    ),
    path(
        "meter_list/apartment=<apartment_id>",
        MeterViewList.as_view(),
        name="meter-view-list-apart",
    ),
    path("", MeterList.as_view(), name="meter-list"),
]
