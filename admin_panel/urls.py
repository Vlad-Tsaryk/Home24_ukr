from django.urls import path, include
from admin_panel.views import index
from admin_purpose.views import PaymentDetailsUpdate

urlpatterns = [
    path('', index, name='statistic'),
    path('users/', include('users.urls')),
    path('service/', include('admin_service.urls')),
    path('purpose/', include('admin_purpose.urls')),
    path('tariff/', include('admin_tariff.urls')),
    path('house/', include('admin_house.urls')),
    path('owner/', include('admin_owner.urls')),
    path('payment_details/', PaymentDetailsUpdate.as_view(), name='payment_details_update'),
]
