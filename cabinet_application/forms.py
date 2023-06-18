from django import forms

from admin_apartment.models import Apartment
from admin_application.forms import ApartmentModelChoiceField
from admin_application.models import Application


class CabinetApplicationForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 8}),
        required=False,
    )
    apartment = ApartmentModelChoiceField(
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="",
        queryset=Apartment.objects.all(),
        required=False,
    )
    master_type = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "form-control"}),
        choices=Application.MasterType.choices,
        required=False,
    )
    date = forms.DateField(widget=forms.DateInput(attrs={"class": "form-control"}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        owner_id = kwargs.pop("owner_id", None)
        super(CabinetApplicationForm, self).__init__(*args, **kwargs)
        self.fields["apartment"].queryset = Apartment.objects.filter(owner_id=owner_id)

    class Meta:
        model = Application
        fields = ["date", "time", "description", "apartment", "master_type"]
