from django.urls import path
from .views import Users, CreateUser, UpdateUser

urlpatterns = [
    path('', Users.as_view(), name='user_list'),
    path('create_user/', CreateUser.as_view(), name='create_user'),
    path('update_user/<pk>/', UpdateUser.as_view(), name='update_user'),
    path('test/', CreateUser.as_view(), name='create_user'),
]
