from django.urls import path
from .views import Users, CreateUser, UpdateUser, ViewUser, delete_user, UpdateRoles

urlpatterns = [
    path('', Users.as_view(), name='user_list'),
    path('create_user/', CreateUser.as_view(), name='create_user'),
    path('update_user/<pk>/', UpdateUser.as_view(), name='update_user'),
    path('user/<pk>/', ViewUser.as_view(), name='view_user'),
    path('roles/', UpdateRoles.as_view(), name='roles'),
    path('delete_user/<user_id>/', delete_user, name='delete_user'),
]
