from django import forms

from admin_tariff.models import Tariff
from .models import Receipt
from admin_apartment.models import Apartment
from admin_house.models import House, Section


class ReceiptForm(forms.ModelForm):
    number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    date = forms.DateField(widget=forms.DateInput(
        attrs={'class': "form-control datetimepicker-input"}))
    house = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control select2-field'}), empty_label='',
                                   queryset=House.objects.all(), required=False)
    section = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control select2-field'}), empty_label='',
                                     queryset=Section.objects.all())
    apartment = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control select2-field'}), empty_label='',
                                       queryset=Apartment.objects.all())
    tariff = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control select2-field'}), empty_label='',
                                    queryset=Tariff.objects.all())
    status = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control'}, choices=Receipt.StatusName.choices),
        initial=Receipt.StatusName.NOT_PAID)
    period_start = forms.DateField(widget=forms.DateInput(
        attrs={'class': "form-control datetimepicker-input"}))
    period_end = forms.DateField(widget=forms.DateInput(
        attrs={'class': "form-control datetimepicker-input"}))
    personal_account = forms.CharField(widget=forms.TextInput({'class': 'form-control'}), required=False)

    def __init__(self, *args, **kwargs):
        super(ReceiptForm, self).__init__(*args, **kwargs)
        if not self.initial.get('number'):
            try:
                self.initial['number'] = str(Receipt.objects.first().pk + 1).zfill(11)
            except:
                self.initial['number'] = '1'.zfill(11)

    class Meta:
        model = Receipt
        fields = '__all__'
