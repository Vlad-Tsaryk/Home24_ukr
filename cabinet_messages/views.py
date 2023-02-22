from django.shortcuts import render
from django.views.generic import ListView, DetailView

from admin_messages.models import Message
from users.mixins import OwnerPermissionRequiredMixin


# Create your views here.
class MessageList(OwnerPermissionRequiredMixin, ListView):
    model = Message
    template_name = 'cabinet_messages/message_list.html'
    ordering = '-created'

    def get_queryset(self):
        return Message.objects.select_related('sender').filter(receivers=self.request.user).order_by(self.ordering)


class MessageView(OwnerPermissionRequiredMixin, DetailView):
    model = Message
    template_name = 'cabinet_messages/message_view.html'
