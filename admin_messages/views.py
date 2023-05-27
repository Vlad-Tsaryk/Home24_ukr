from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, DeleteView

from admin_apartment.models import Apartment
from admin_house.models import Section, Floor
from admin_messages.forms import MessageForm
from admin_personal_account.models import PersonalAccount
from users.models import User
from users.mixins import AdminPermissionRequiredMixin
from admin_messages.models import Message


# Create your views here.
class MessageCreate(AdminPermissionRequiredMixin, CreateView):
    permission_required = 'messages'
    model = Message
    form_class = MessageForm
    template_name = 'admin_messages/admin_messages_create.html'
    success_url = reverse_lazy('message_list')

    def get_form_kwargs(self):
        if self.kwargs.get('has_debt'):
            self.initial = {'owners_has_debt': True}
        return super(MessageCreate, self).get_form_kwargs()

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
        if self.request.POST.get('owners_has_debt'):
            owner_list = []
            for owner in owners:
                if owner not in owner_list:
                    if PersonalAccount.owner_has_debt(owner_id=owner.id):
                        owner_list.append(owner)
            form.receivers.add(*owner_list)
        else:
            form.receivers.add(*owners)
        self.object = form
        messages.success(self.request, 'Сообщение успішно создано')
        return HttpResponseRedirect(self.get_success_url())


class MessageCreateOwner(MessageCreate):
    template_name = 'admin_messages/admin_message_create_user.html'

    def get_form_kwargs(self):
        if self.kwargs.get('owner_id'):
            self.initial = {'receiver': self.kwargs.get('owner_id')}
        return super(MessageCreateOwner, self).get_form_kwargs()

    def form_valid(self, form):
        form = form.save(commit=False)
        form.sender = self.request.user
        form.save()
        if self.request.POST.get('receiver'):
            form.receivers.add(self.request.POST.get('receiver'))
        messages.success(self.request, 'Сообщение успішно создано')
        return HttpResponseRedirect(self.success_url)


class MessageList(AdminPermissionRequiredMixin, ListView):
    permission_required = 'messages'
    model = Message
    template_name = 'admin_messages/admin_messages_list.html'
    ordering = '-created'

    def get_queryset(self):
        return Message.objects.select_related('house', 'section', 'floor',
                                              'apartment').prefetch_related('receivers').order_by(self.ordering)

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            search_value = self.request.GET.get('search[value]')
            filtered_qs = self.get_queryset().filter(Q(text__contains=search_value) | Q(subject__contains=search_value))
            result_list = list(filtered_qs.values('id', 'text', 'subject', 'created'))
            for message in result_list:
                message['receivers'] = filtered_qs.get(id=message['id']).get_receiver_label
            start = int(self.request.GET.get('start', 0))
            length = int(self.request.GET.get('length', 10))
            paginator = Paginator(result_list, self.request.GET.get('length', 10))
            page = (start // length) + 1
            data = list(paginator.get_page(page))
            result = {
                'data': data,
                'recordsTotal': paginator.count,
                'recordsFiltered': paginator.count,
                'pages': paginator.num_pages,
            }
            return JsonResponse(result, safe=False, **response_kwargs)
        else:
            return super(ListView, self).render_to_response(context, **response_kwargs)


class MessageView(AdminPermissionRequiredMixin, DetailView):
    permission_required = 'messages'
    model = Message
    template_name = 'admin_messages/admin_messages_view.html'


class MessageDelete(AdminPermissionRequiredMixin, DeleteView):
    permission_required = 'messages'
    model = Message
    success_message = 'Сообщение удалено успішно'
    success_url = reverse_lazy('message_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class MessageDeleteMany(AdminPermissionRequiredMixin, View):
    permission_required = 'messages'

    def delete(self, request, *args, **kwargs):
        object_list = self.request.POST.getlist('selected_messages[]')
        for obj_pk in object_list:
            Message.objects.get(pk=obj_pk).delete()
        messages.success(self.request, 'Сообщения удалены успішно')
        return HttpResponse('Success')

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
