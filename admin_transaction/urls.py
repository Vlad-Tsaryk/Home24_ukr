from django.urls import path, re_path

from .views import TransactionCreate

urlpatterns = [
    # path('', ApplicationList.as_view(), name='application_list'),
    # re_path(r'^create/(?:type=(?P<transaction_type>[a-z]+)/)?$', TransactionCreate.as_view(),
    #         name='transaction_create'),
    path('create/type=<transaction_type>', TransactionCreate.as_view(),
            name='transaction_create'),
]