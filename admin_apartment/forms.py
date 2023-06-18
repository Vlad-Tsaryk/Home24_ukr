from django import forms
from django.core.exceptions import ValidationError

from admin_personal_account.models import PersonalAccount
from .models import Apartment
from admin_house.models import House, Section, Floor
from users.models import User, Role
from admin_tariff.models import Tariff


class ApartmentForm(forms.ModelForm):
    number = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control"}), min_value=0
    )
    area = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        min_value=0,
        required=False,
    )
    house = forms.ModelChoiceField(
        widget=forms.Select(attrs={"class": "form-control"}),
        queryset=House.objects.all(),
        empty_label="Оберіть...",
    )
    section = forms.ModelChoiceField(
        widget=forms.Select(attrs={"class": "form-control"}),
        queryset=Section.objects.all(),
        empty_label="Оберіть...",
        required=False,
    )
    floor = forms.ModelChoiceField(
        widget=forms.Select(attrs={"class": "form-control"}),
        queryset=Floor.objects.all(),
        empty_label="Оберіть...",
        required=False,
    )
    owner = forms.ModelChoiceField(
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="Оберіть...",
        queryset=User.objects.filter(role=Role.objects.get(role=Role.RoleName.OWNER)),
        required=False,
    )
    tariff = forms.ModelChoiceField(
        widget=forms.Select(attrs={"class": "form-control"}),
        queryset=Tariff.objects.all(),
        empty_label="Оберіть...",
        required=False,
    )
    personal_account_select = forms.ModelChoiceField(
        widget=forms.Select(attrs={"class": "form-control"}),
        queryset=PersonalAccount.objects.filter(apartment__isnull=True),
        empty_label="Оберіть...",
        required=False,
    )
    personal_account = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        super(ApartmentForm, self).__init__(*args, **kwargs)
        instance = kwargs.get("instance")
        if instance:
            try:
                self.fields["personal_account"].initial = PersonalAccount.objects.get(
                    apartment_id=instance.pk
                ).number
            except PersonalAccount.DoesNotExist:
                pass

    def clean_personal_account(self):
        number = self.cleaned_data["personal_account"]
        if number:
            self.cleaned_data["personal_account_create"] = True
            if PersonalAccount.objects.filter(
                number=number, apartment__isnull=False
            ).exists():
                raise ValidationError("Особовий рахунок вже використовується")
            elif PersonalAccount.objects.filter(number=number).exists():
                self.cleaned_data["personal_account_create"] = False
        return number

    class Meta:
        model = Apartment
        fields = "__all__"
