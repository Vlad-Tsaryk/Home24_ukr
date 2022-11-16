from django.contrib import admin
from .models import TariffService, Tariff
# Register your models here.
admin.site.register(TariffService)
admin.site.register(Tariff)