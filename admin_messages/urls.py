from django.urls import path

from admin_messages.views import MessageCreate, MessageList, MessageView, MessageDelete, MessageDeleteMany

urlpatterns = [
    path('create/', MessageCreate.as_view(), name='message_create'),
    path('delete/<pk>', MessageDelete.as_view(), name='message_delete'),
    path('delete_many/', MessageDeleteMany.as_view(), name='message_delete_many'),
    path('<pk>', MessageView.as_view(), name='message_view'),
    path('', MessageList.as_view(), name='message_list'),
]
