from django import forms
from .models import PersonalAccount, Apartment
from admin_house.models import House


class PersonalAccountForm(forms.ModelForm):
    status = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                               choices=PersonalAccount.StatusName.choices)
    apartment = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), empty_label='',
                                       queryset=Apartment.objects.all(), required=False)
    house = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), empty_label='',
                                   queryset=House.objects.all())

    class Meta:
        model = PersonalAccount
        fields = ['status', 'apartment']
