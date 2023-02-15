from django.urls import path

from admin_messages.views import MessageCreate, MessageList, MessageView, MessageDelete, MessageDeleteMany,\
    MessageCreateOwner

urlpatterns = [
    path('create/', MessageCreate.as_view(), name='message_create'),
    path('create/owner_id=<owner_id>', MessageCreateOwner.as_view(), name='message_create_owner'),
    path('create/has_debt=<has_debt>', MessageCreate.as_view(), name='message_create_has_debt'),
    path('delete/<pk>', MessageDelete.as_view(), name='message_delete'),
    path('delete_many/', MessageDeleteMany.as_view(), name='message_delete_many'),
    path('<pk>', MessageView.as_view(), name='message_view'),
    path('', MessageList.as_view(), name='message_list'),
]
