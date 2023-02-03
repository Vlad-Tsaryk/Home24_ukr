from django import forms

from excel_templates.models import ExcelTemplate


class ExcelTemplateCreateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = ExcelTemplate
        fields = '__all__'
        exclude = ['default', ]
