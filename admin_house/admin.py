from django.contrib import admin
from .models import House, Section, Floor, HouseUser

# Register your models here.
admin.site.register(House)
admin.site.register(Section)
admin.site.register(Floor)
admin.site.register(HouseUser)
