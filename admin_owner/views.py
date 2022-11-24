from django.shortcuts import render
from django.views.generic import CreateView, UpdateView
from users.models import User
from .forms import OwnerChangeForm, OwnerCreateForm


# Create your views here.

class OwnerCreate(CreateView):
    model = User
    template_name = 'admin_owner/owner_create.html'
    form_class = OwnerCreateForm


class OwnerUpdate(UpdateView):
    model = User
    template_name = 'admin_owner/owner_update.html'
    form_class = OwnerChangeForm
    context_object_name = 'owner'
