from django import forms
from .models import Apartment
from admin_house.models import House, Section, Floor
from users.models import User, Role
from admin_tariff.models import Tariff


class ApartmentForm(forms.ModelForm):
    number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), min_value=0)
    area = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), min_value=0, required=False)
    house = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), queryset=House.objects.all(),
                                   empty_label='Выберите...')
    section = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                     queryset=Section.objects.all(), empty_label='Выберите...', required=False)
    floor = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                   queryset=Floor.objects.all(), empty_label='Выберите...', required=False)
    owner = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), empty_label='Выберите...',
                                   queryset=User.objects.filter(role=Role.objects.get(role=Role.RoleName.OWNER)),
                                   required=False)
    tariff = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                    queryset=Tariff.objects.all(), empty_label='Выберите...', required=False)

    class Meta:
        model = Apartment
        fields = '__all__'
