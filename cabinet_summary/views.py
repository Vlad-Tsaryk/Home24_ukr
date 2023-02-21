from django.shortcuts import render
from django.views.generic import DetailView

from admin_apartment.models import Apartment


# Create your views here.
class ApartmentSummary(DetailView):
    model = Apartment
    template_name = 'cabinet_summary/apartment_summary.html'
