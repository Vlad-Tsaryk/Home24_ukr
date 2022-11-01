from django.urls import path
from .views import Users, CreateUser

urlpatterns = [
    path('', Users.as_view(), name='user_list'),
    path('create_user/', CreateUser.as_view(), name='create_user'),
]
