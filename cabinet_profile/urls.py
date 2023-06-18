from django.urls import path
from .views import ProfileView, ProfileUpdate

urlpatterns = [
    path("", ProfileView.as_view(), name="cabinet_profile"),
    path("update/", ProfileUpdate.as_view(), name="cabinet_profile_update"),
]
