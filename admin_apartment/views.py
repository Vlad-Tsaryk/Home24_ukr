from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from .models import Apartment


# Create your views here.


class ApartmentCreate(CreateView):
    model = Apartment

