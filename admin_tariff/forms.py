from django import forms
from django.forms import modelformset_factory

from .models import Tariff, TariffService
from admin_service.models import Service


class TariffForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}))

    # services = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
    #                                   queryset=Service.objects.all(),
    #                                   required=False)

    class Meta:
        model = Tariff
        fields = '__all__'


class TariffServiceForm(forms.ModelForm):
    price = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}), min_value=0)
    service = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                     queryset=Service.objects.all())

    class Meta:
        model = TariffService
        fields = '__all__'


TariffServiceFormSet = modelformset_factory(model=TariffService, form=TariffServiceForm, extra=0, can_delete=True)
