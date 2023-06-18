from django.urls import path
from .views import (
    ApplicationCreate,
    ApplicationList,
    ApplicationView,
    ApplicationUpdate,
    application_delete,
)

urlpatterns = [
    path("", ApplicationList.as_view(), name="application_list"),
    path("create/", ApplicationCreate.as_view(), name="application_create"),
    path("update/<pk>", ApplicationUpdate.as_view(), name="application_update"),
    path("<pk>", ApplicationView.as_view(), name="application_view"),
    path("delete/<pk>", application_delete, name="application_delete"),
]
