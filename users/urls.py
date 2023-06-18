from django.urls import path
from .views import (
    Users,
    CreateUser,
    UpdateUser,
    ViewUser,
    DeleteUser,
    UpdateRoles,
    InviteUser,
)

urlpatterns = [
    path("", Users.as_view(), name="user_list"),
    path("create_user/", CreateUser.as_view(), name="create_user"),
    path("update_user/<pk>/", UpdateUser.as_view(), name="update_user"),
    path("user/<pk>/", ViewUser.as_view(), name="view_user"),
    path("roles/", UpdateRoles.as_view(), name="roles"),
    path("delete_user/<pk>/", DeleteUser.as_view(), name="delete_user"),
    path("invite_user/<pk>/", InviteUser.as_view(), name="invite_user"),
]
