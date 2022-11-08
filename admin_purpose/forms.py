from django import forms
from .models import PaymentDetails, Purpose


class PaymentDetailsForm(forms.ModelForm):
    info = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}), required=False)
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=128,
                           required=False)

    class Meta:
        model = PaymentDetails
        fields = '__all__'


class PurposeForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=50,
                           required=False)
    transaction_type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                         choices=Purpose.TransactionType.choices)

    class Meta:
        model = Purpose
        fields = '__all__'
