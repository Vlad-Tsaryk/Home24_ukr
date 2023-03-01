from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models.functions import Concat
from django.db.models import Value
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView

from admin_personal_account.models import PersonalAccount
from users.mixins import AdminPermissionRequiredMixin
from .models import Apartment, Section, Floor, House
from .forms import ApartmentForm
from django.contrib import messages


# Create your views here.

def apartment_house_details(house_id, **response_kwargs):
    section_list = list(Section.objects.filter(house=house_id).values())
    floor_list = list(Floor.objects.filter(house=house_id).values())
    return JsonResponse({'section': section_list, 'floor': floor_list}, safe=False, **response_kwargs)


class ApartmentCreate(AdminPermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'apartments'
    model = Apartment
    template_name = 'admin_apartment/apartment_create.html'
    form_class = ApartmentForm
    success_message = "Квартира успешно создана"
    success_url = reverse_lazy('apartment_list')

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            house_id = self.request.GET.get('house_id')
            if house_id:
                return apartment_house_details(house_id, **response_kwargs)
        else:
            return super(CreateView, self).render_to_response(context, **response_kwargs)

    def form_valid(self, form):
        self.object = form.save()
        if form.cleaned_data['personal_account']:
            if form.cleaned_data['personal_account_create']:
                PersonalAccount.objects.create(number=form.cleaned_data['personal_account'],
                                               apartment=self.object, status=PersonalAccount.StatusName.ACTIVE)
            else:
                personal_account = PersonalAccount.objects.get(
                    number=form.cleaned_data['personal_account']).apartment = form
                personal_account.save()
        return super().form_valid(form)


class ApartmentUpdate(AdminPermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'apartments'
    model = Apartment
    template_name = 'admin_apartment/apartment_update.html'
    form_class = ApartmentForm
    success_message = "Квартира успешно обновлена"
    success_url = reverse_lazy('apartment_list')

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            house_id = self.request.GET.get('house_id')
            if house_id:
                return apartment_house_details(house_id, **response_kwargs)
        else:
            return super(UpdateView, self).render_to_response(context, **response_kwargs)

    def form_valid(self, form):
        self.object = form.save()
        if form.cleaned_data['personal_account']:
            if form.cleaned_data['personal_account_create']:
                PersonalAccount.objects.create(number=form.cleaned_data['personal_account'],
                                               apartment=self.object, status=PersonalAccount.StatusName.ACTIVE)
            else:
                personal_account = PersonalAccount.objects.get(number=form.cleaned_data['personal_account'])
                personal_account.apartment = self.object
                personal_account.save()
        return super().form_valid(form)


class ApartmentView(AdminPermissionRequiredMixin, DetailView):
    permission_required = 'apartments'
    model = Apartment
    template_name = 'admin_apartment/apartment_view.html'


def apartment_delete(request, pk):
    name = None
    try:
        obj_delete = Apartment.objects.get(pk=pk)
        n = obj_delete.__str__()
        if obj_delete.delete():
            name = n
    except:
        messages.error(request, f"Не удалось удалить квартиру")
    if name:
        messages.success(request, f"Квартира {name} удалена успешно")
    return redirect('apartment_list')


class ApartmentList(AdminPermissionRequiredMixin, ListView):
    permission_required = 'apartments'
    model = Apartment
    template_name = 'admin_apartment/apartment_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ApartmentList, self).get_context_data(**kwargs)
        context['house_list'] = House.objects.all()
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            print(self.request.GET)
            result = {'apartment': ''}
            filter_fields = {
                'number__contains': self.request.GET.get('number'),
                'house': self.request.GET.get('house'),
                'section': self.request.GET.get('section'),
                'floor': self.request.GET.get('floor'),
                'owner': self.request.GET.get('owner'),
            }
            if self.request.GET.get('house_select'):
                result['sections'] = list(Section.objects.filter(house=filter_fields['house']).values())
                result['floors'] = list(Floor.objects.filter(house=filter_fields['house']).values())

            filter_fields = {k: v for k, v in filter_fields.items() if v}
            filtered_qs = self.get_queryset().filter(**filter_fields)
            order_field = self.request.GET.get('order_by')
            filtered_qs = filtered_qs.annotate(
                owner__name=Concat('owner__first_name', Value(' '),
                                   'owner__middle_name', Value(' '),
                                   'owner__last_name'))
            if order_field:
                filtered_qs = filtered_qs.order_by(order_field)

            filtered_qs = filtered_qs.values('id', 'number', 'house__name', 'floor__name', 'section__name',
                                             'owner__name')

            start = int(self.request.GET.get('start', 0))
            length = int(self.request.GET.get('length', 10))
            paginator = Paginator(filtered_qs, self.request.GET.get('length', 10))
            page = (start // length) + 1
            data = list(paginator.get_page(page))
            for apartment in data:
                try:
                    apartment['balance'] = PersonalAccount.objects.get(apartment_id=apartment['id']).balance
                except PersonalAccount.DoesNotExist:
                    apartment['balance'] = '(нет счета)'
            result['apartment'] = data
            result['recordsTotal'] = paginator.count
            result['recordsFiltered'] = paginator.count
            result['pages'] = paginator.num_pages
            return JsonResponse(result, safe=False, **response_kwargs)

        else:
            return super(ListView, self).render_to_response(context, **response_kwargs)
