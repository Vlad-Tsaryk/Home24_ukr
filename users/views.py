from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from .models import User, Role
from .forms import CustomUserCreationForm, CustomUserUpdateForm


# Create your views here.

class Users(ListView):
    model = User
    context_object_name = 'user_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Users, self).get_context_data(**kwargs)
        context['admin'] = User.objects.get(is_superuser=True)
        return context


class CreateUser(CreateView):
    form_class = CustomUserCreationForm
    # template_name = 'users/create_user.html'
    template_name = 'users/test.html'
    success_url = reverse_lazy('user_list')


class UpdateUser(UpdateView):
    model = User
    form_class = CustomUserUpdateForm
    template_name = 'users/update_user.html'
    success_url = reverse_lazy('user_list')

