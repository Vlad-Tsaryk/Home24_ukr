from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from admin_owner.forms import OwnerChangeForm, CabinetOwnerChangeForm
from users.mixins import OwnerPermissionRequiredMixin
from users.models import User


# Create your views here.
class ProfileView(OwnerPermissionRequiredMixin, DetailView):
    model = User
    template_name = "cabinet_profile/profile_view.html"
    context_object_name = "owner"

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context["apartments"] = self.object.apartment_set.select_related(
            "floor", "house", "section", "personalaccount"
        )
        return context

    def get_object(self, queryset=None):
        return self.request.user


class ProfileUpdate(OwnerPermissionRequiredMixin, UpdateView, SuccessMessageMixin):
    model = User
    template_name = "cabinet_profile/profile_update.html"
    form_class = OwnerChangeForm
    success_message = "Власника квартири успішно оновлено"
    context_object_name = "owner"
    success_url = reverse_lazy("cabinet_profile")

    def get_object(self, queryset=None):
        return self.request.user
