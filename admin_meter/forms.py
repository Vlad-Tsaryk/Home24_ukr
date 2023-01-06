from django import forms

from admin_apartment.models import Apartment
from admin_house.models import House, Section
from .models import Meter
from admin_service.models import Service


class MeterForm(forms.ModelForm):
    service = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), empty_label='',
                                     queryset=Service.objects.filter(is_counter=True), required=False)
    number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    date = forms.DateField(widget=forms.DateInput(
        attrs={'class': "form-control datetimepicker-input",
               'data-target': '#reservationdate'}))
    apartment = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), empty_label='',
                                       queryset=Apartment.objects.all(), required=False)
    house = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), empty_label='',
                                   queryset=House.objects.all(), required=False)
    section = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), empty_label='',
                                     queryset=Section.objects.all(), required=False)
    value = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}))
    status = forms.CharField(widget=forms.Select(attrs={'class': 'form-control'}, choices=Meter.StatusName.choices))

    def __init__(self, *args, **kwargs):
        super(MeterForm, self).__init__(*args, **kwargs)
        self.initial['number'] = str(Meter.objects.last().pk + 1).zfill(11)
        try:
            if self.instance.apartment:
                self.initial['house'] = self.instance.apartment.house_id
                self.initial['section'] = self.instance.apartment.section_id
                print(self.instance.apartment)
        except:
            pass

    class Meta:
        model = Meter
        fields = ['service', 'apartment', 'status', 'value', 'date', 'number']
