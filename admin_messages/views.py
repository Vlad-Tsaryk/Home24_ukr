from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, DeleteView

from admin_apartment.models import Apartment
from admin_house.models import Section, Floor
from admin_messages.forms import MessageForm
from users.models import User
from admin_messages.models import Message


# Create your views here.
class MessageCreate(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'admin_messages/admin_messages_create.html'
    success_url = reverse_lazy('message_list')

    # def delete_messages(self):
    #     delete_info = {
    #         'success_msg': [],
    #         'error_msg': [],
    #     }
    #     for pk in self.request.GET.getlist('selection[]'):
    #         try:
    #             obj_delete = Message.objects.get(pk=pk)
    #             if obj_delete.delete():
    #                 delete_info['success_msg'].append(f"Сообщение успешно удалено")
    #         except:
    #             delete_info['error_msg'].append(f"Не удалось удалить сообщение")
    #     return delete_info

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            result = {}
            house_id = self.request.GET.get('house_id')
            section_id = self.request.GET.get('section_id')
            floor_id = self.request.GET.get('floor_id')
            print(self.request.GET)
            apartment_filters = {}
            if house_id:
                apartment_filters['house'] = house_id
                if floor_id:
                    apartment_filters['floor'] = floor_id
                else:
                    result['floors'] = list(Floor.objects.filter(house=house_id).values('id', 'name'))
                if section_id:
                    apartment_filters['section'] = section_id
                else:
                    result['sections'] = list(Section.objects.filter(house=house_id).values('id', 'name'))
                result['apartments'] = list(Apartment.objects.filter(**apartment_filters).values('id', 'number'))
            return JsonResponse(result, safe=False, **response_kwargs)
        else:
            return super(CreateView, self).render_to_response(context, **response_kwargs)

    def form_valid(self, form):

        form = form.save(commit=False)
        form.sender = self.request.user
        form.save()
        owner_filters = {
            'apartment__house': form.house,
            'apartment__section': form.section,
            'apartment__floor': form.floor,
            'apartment': form.apartment,
        }
        owner_filters = {k: v for k, v in owner_filters.items() if v}
        owners = User.get_owners().filter(**owner_filters)
        form.receivers.add(*owners)
        self.object = form
        # messages.success(self.request, 'Сообщение успешно создано')
        return HttpResponseRedirect(self.get_success_url())


class MessageList(ListView):
    model = Message
    template_name = 'admin_messages/admin_messages_list.html'
    ordering = '-created'


class MessageView(DetailView):
    model = Message
    template_name = 'admin_messages/admin_messages_view.html'


class MessageDelete(DeleteView):
    model = Message
    success_message = 'Сообщение удалено успешно'
    success_url = reverse_lazy('message_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

