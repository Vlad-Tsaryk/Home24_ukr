from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.contrib import messages
from .forms import HouseForm
from .models import House, Section, Floor
from users.models import User


# Create your views here.

class HouseCreate(CreateView):
    model = House
    template_name = 'admin_house/house_create.html'
    form_class = HouseForm
