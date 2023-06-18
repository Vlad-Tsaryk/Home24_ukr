from django.urls import path
from .views import PurposeCreate, PurposeList, PurposeUpdate, purpose_delete

urlpatterns = [
    path("create/", PurposeCreate.as_view(), name="purpose_create"),
    path("update/<pk>/", PurposeUpdate.as_view(), name="purpose_update"),
    path("delete/<pk>/", purpose_delete, name="purpose_delete"),
    path("", PurposeList.as_view(), name="purpose_list"),
]
