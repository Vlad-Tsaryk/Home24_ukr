from django.urls import path
from .views import ExcelTemplateCreate, ExcelTemplateDelete, ExcelTemplateSetDefault
urlpatterns = [
    path('', ExcelTemplateCreate.as_view(), name='excel-template-create'),
    path('delete/<pk>', ExcelTemplateDelete.as_view(), name='excel-template-delete'),
    path('set_default/<pk>', ExcelTemplateSetDefault.as_view(), name='excel-template-set-default'),
]