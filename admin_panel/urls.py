from django.urls import path
from admin_panel.views import index

urlpatterns = [
    path('', index, name='statistic'),
]
