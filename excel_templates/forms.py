from django import forms

from excel_templates.models import ExcelTemplate
from django.core.validators import FileExtensionValidator


class ExcelTemplateCreateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    file = forms.FileField(widget=forms.FileInput(attrs={
        'accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel'}),
        validators=[FileExtensionValidator(allowed_extensions=["xlsx"], message='Только файлы MicrosoftExcel')])

    class Meta:
        model = ExcelTemplate
        fields = ['name', 'file']
        exclude = ['default', ]
