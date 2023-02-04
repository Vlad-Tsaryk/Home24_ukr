from django.urls import path
from .views import ExcelTemplateCreate, ExcelTemplateDelete, ExcelTemplateSetDefault, ExcelTemplatePrint
urlpatterns = [
    path('', ExcelTemplateCreate.as_view(), name='excel-template-create'),
    path('print/<pk>', ExcelTemplatePrint.as_view(), name='excel-template-print'),
    path('delete/<pk>', ExcelTemplateDelete.as_view(), name='excel-template-delete'),
    path('set_default/<pk>', ExcelTemplateSetDefault.as_view(), name='excel-template-set-default'),
]