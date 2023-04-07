from django.urls import path, include
from admin_panel.views import StatisticView
from admin_purpose.views import PaymentDetailsUpdate
from django.conf.urls import handler404
from django.contrib.auth.decorators import login_required

from users.views import AdminLoginView, AdminLogoutView

urlpatterns = [
    path('', StatisticView.as_view(), name='statistic'),
    path('site/login/', AdminLoginView.as_view(), name='admin-panel-login'),
    path('site/logout/', AdminLogoutView.as_view(), name='admin-panel-logout'),
    path('users/', include('users.urls')),
    path('service/', include('admin_service.urls')),
    path('purpose/', include('admin_purpose.urls')),
    path('tariff/', include('admin_tariff.urls')),
    path('house/', include('admin_house.urls')),
    path('owner/', include('admin_owner.urls')),
    path('apartment/', include('admin_apartment.urls')),
    path('account/', include('admin_personal_account.urls')),
    path('meter/', include('admin_meter.urls')),
    path('application/', include('admin_application.urls')),
    path('transaction/', include('admin_transaction.urls')),
    path('receipt/', include('admin_receipt.urls')),
    path('message/', include('admin_messages.urls')),
    path('website/', include('admin_website.urls')),
    path('payment_details/', PaymentDetailsUpdate.as_view(), name='payment_details_update'),
]

handler404 = 'admin_panel.views.error_404'
