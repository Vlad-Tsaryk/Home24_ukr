from django.urls import path
from .views import MessageList, MessageView
urlpatterns = [
    path('', MessageList.as_view(), name='cabinet_message_list'),
    path('<pk>', MessageView.as_view(), name='cabinet_message_view'),
]
