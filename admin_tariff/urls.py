from django.urls import path
from .views import (
    TariffCreate,
    TariffList,
    TariffClone,
    TariffUpdate,
    TariffView,
    delete_tariff,
)

urlpatterns = [
    path("", TariffList.as_view(), name="tariff_list"),
    path("create/", TariffCreate.as_view(), name="tariff_create"),
    path("clone/tariff_id=<pk>", TariffClone.as_view(), name="tariff_clone"),
    path("update/<pk>", TariffUpdate.as_view(), name="tariff_update"),
    path("<pk>", TariffView.as_view(), name="tariff_view"),
    path("delete/<pk>", delete_tariff, name="tariff_delete"),
]
