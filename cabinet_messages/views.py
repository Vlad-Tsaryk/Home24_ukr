from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.http import JsonResponse
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

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            search_value = self.request.GET.get('search[value]')
            filtered_qs = self.get_queryset().filter(Q(text__contains=search_value) | Q(subject__contains=search_value))
            result_list = list(
                filtered_qs
                .annotate(sender_name=Concat('sender__first_name', Value(' '), 'sender__last_name'))
                .values('id', 'text', 'subject', 'created', 'sender_name'))

            start = int(self.request.GET.get('start', 0))
            length = int(self.request.GET.get('length', 10))
            paginator = Paginator(result_list, self.request.GET.get('length', 10))
            page = (start // length) + 1
            data = list(paginator.get_page(page))
            print(data)
            result = {
                'data': data,
                'recordsTotal': paginator.count,
                'recordsFiltered': paginator.count,
                'pages': paginator.num_pages,
            }
            return JsonResponse(result, safe=False, **response_kwargs)
        else:
            return super(ListView, self).render_to_response(context, **response_kwargs)


class MessageView(OwnerPermissionRequiredMixin, DetailView):
    model = Message
    template_name = 'cabinet_messages/message_view.html'
