from django.urls import path, include
from users.views import CabinetLoginView

urlpatterns = [
    path('site/login/', CabinetLoginView.as_view(), name='cabinet_login'),
    path('profile/', include('cabinet_profile.urls')),
    path('tariff/', include('cabinet_tariff.urls')),
    path('message/', include('cabinet_messages.urls')),
    path('receipt/', include('cabinet_receipts.urls')),
    path('application/', include('cabinet_application.urls')),
    # path('', StatisticView.as_view(), name='statistic'),
]
