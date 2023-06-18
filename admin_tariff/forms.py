from django import forms
from django.forms import modelformset_factory, formset_factory

from .models import Tariff, TariffService
from admin_service.models import Service


class TariffForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": "5"})
    )

    # services = forms.ModelChoiceField(required=False, queryset=Service.objects.all())

    class Meta:
        model = Tariff
        fields = "__all__"
        exclude = [
            "services",
        ]


class TariffServiceForm(forms.ModelForm):
    price = forms.FloatField(
        widget=forms.NumberInput(attrs={"class": "form-control price", "step": "0.5"}),
        min_value=0,
        required=True,
    )
    service = forms.ModelChoiceField(
        widget=forms.Select(attrs={"class": "form-control service"}),
        queryset=Service.objects.all(),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(TariffServiceForm, self).__init__(*args, **kwargs)
        self.fields["tariff"].required = False

    class Meta:
        model = TariffService
        fields = ["service", "price", "tariff"]


# TariffServiceFormSet = formset_factory(form=TariffServiceForm, extra=0, can_delete=True)
TariffServiceFormSet = modelformset_factory(
    model=TariffService, form=TariffServiceForm, extra=0, can_delete=True
)
