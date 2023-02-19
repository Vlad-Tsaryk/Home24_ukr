from django.shortcuts import render
from django.views.generic import ListView, DetailView

from admin_messages.models import Message


# Create your views here.
class MessageList(ListView):
    model = Message
    template_name = 'cabinet_messages/message_list.html'

    def get_queryset(self):
        return Message.objects.select_related('sender').filter(receivers=self.request.user)


class MessageView(DetailView):
    model = Message
    template_name = 'cabinet_messages/message_view.html'
