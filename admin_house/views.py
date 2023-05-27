from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.contrib import messages

from users.mixins import AdminPermissionRequiredMixin
from .forms import HouseForm, SectionFormSet, FloorFormSet, HouseUserFormSet
from .models import House, Section, Floor, HouseUser


# Create your views here.
class HouseList(AdminPermissionRequiredMixin, ListView):
    permission_required = 'applications'
    model = House
    template_name = 'admin_house/house_list.html'

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            filtered_qs = self.get_queryset()
            print(self.request.GET)
            filter_fields = {
                'name__contains': self.request.GET.get('name'),
                'address__contains': self.request.GET.get('address'),
            }
            filter_fields = {k: v for k, v in filter_fields.items() if v}
            filtered_qs = filtered_qs.filter(**filter_fields)
            if self.request.GET.get('order_by'):
                filtered_qs = filtered_qs.order_by(self.request.GET.get('order_by'))

            filtered_qs = filtered_qs.values('id', 'name', 'address')
            start = int(self.request.GET.get('start', 0))
            length = int(self.request.GET.get('length', 10))
            paginator = Paginator(filtered_qs, self.request.GET.get('length', 10))
            page = (start // length) + 1
            data = list(paginator.get_page(page))
            result = {
                'data': data,
                'recordsTotal': paginator.count,
                'recordsFiltered': paginator.count,
                'pages': paginator.num_pages,
            }
            print(result)
            return JsonResponse(result, safe=False, **response_kwargs)
        else:
            return super(ListView, self).render_to_response(context, **response_kwargs)


class HouseView(AdminPermissionRequiredMixin, DetailView):
    permission_required = 'houses'
    model = House
    template_name = 'admin_house/house_view.html'


def house_delete(request, pk):
    obj_house = House.objects.get(pk=pk)
    messages.success(request, f"Будинок {obj_house.name} успішно удалён")
    obj_house.delete()
    return redirect('house_list')


class HouseCreate(AdminPermissionRequiredMixin, CreateView):
    permission_required = 'houses'
    model = House
    template_name = 'admin_house/house_create.html'
    form_class = HouseForm
    success_url = 'house_list'

    def get_context_data(self, **kwargs):
        context = super(HouseCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['section_formset'] = SectionFormSet(self.request.POST, prefix='section')
            context['floor_formset'] = FloorFormSet(self.request.POST, prefix='floor')
            context['house_user_formset'] = HouseUserFormSet(self.request.POST, prefix='house_user')
        else:
            context['section_formset'] = SectionFormSet(prefix='section', queryset=Section.objects.none())
            context['floor_formset'] = FloorFormSet(prefix='floor', queryset=Floor.objects.none())
            context['house_user_formset'] = HouseUserFormSet(prefix='house_user', queryset=HouseUser.objects.none())
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        context = self.get_context_data()
        floor_formset = context['floor_formset']
        section_formset = context['section_formset']
        house_user_formset = context['house_user_formset']
        if floor_formset.is_valid() and section_formset.is_valid() and form.is_valid() and house_user_formset.is_valid():
            return self.form_valid(form, floor_formset, section_formset, house_user_formset)
        else:
            return super(HouseCreate, self).render_to_response(self.get_context_data())

    def form_valid(self, form, floor_formset, section_formset, house_user_formset):
        house = form.save()
        floors = floor_formset.save(commit=False)
        sections = section_formset.save(commit=False)
        house_users = house_user_formset.save(commit=False)
        for floor in floors:
            floor.house_id = house.pk
        for section in sections:
            section.house_id = house.pk
        for house_user in house_users:
            house_user.house_id = house.pk
        floor_formset.save()
        section_formset.save()
        house_user_formset.save()
        messages.success(self.request, f"Будинок {house.name} создан успішно")
        return redirect(self.success_url)


class HouseUpdate(AdminPermissionRequiredMixin, UpdateView):
    permission_required = 'houses'
    model = House
    form_class = HouseForm
    template_name = 'admin_house/house_update.html'
    success_url = 'house_list'

    def get_context_data(self, **kwargs):
        context = super(HouseUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['section_formset'] = SectionFormSet(self.request.POST, prefix='section')
            context['floor_formset'] = FloorFormSet(self.request.POST, prefix='floor')
            context['house_user_formset'] = HouseUserFormSet(self.request.POST, prefix='house_user')
        else:
            context['section_formset'] = SectionFormSet(prefix='section',
                                                        queryset=Section.objects.filter(house=self.kwargs['pk']))
            context['floor_formset'] = FloorFormSet(prefix='floor',
                                                    queryset=Floor.objects.filter(house=self.kwargs['pk']))
            context['house_user_formset'] = HouseUserFormSet(prefix='house_user',
                                                             queryset=HouseUser.objects.filter(house=self.kwargs['pk']))
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        context = self.get_context_data()
        floor_formset = context['floor_formset']
        section_formset = context['section_formset']
        house_user_formset = context['house_user_formset']
        if floor_formset.is_valid() and section_formset.is_valid() and form.is_valid() and house_user_formset.is_valid():
            return self.form_valid(form, floor_formset, section_formset, house_user_formset)
        else:
            # print('floor_formset', floor_formset.errors)
            # print('section_formset', section_formset.errors)
            # print('house_user_formset', house_user_formset.errors)
            # print('form', form.errors)
            # print('invalid')
            return super(HouseUpdate, self).render_to_response(self.get_context_data())

    def form_valid(self, form, floor_formset, section_formset, house_user_formset):
        house = form.save()
        floors = floor_formset.save(commit=False)
        sections = section_formset.save(commit=False)
        house_users = house_user_formset.save(commit=False)
        for floor in floors:
            floor.house_id = house.pk
        for section in sections:
            section.house_id = house.pk
        for house_user in house_users:
            house_user.house_id = house.pk
        floor_formset.save()
        section_formset.save()
        house_user_formset.save()
        messages.success(self.request, f"Будинок {house.name} успішно обновлен")
        return redirect(self.success_url)
