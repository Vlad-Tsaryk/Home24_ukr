from django import forms
from admin_apartment.models import Apartment
from admin_house.models import Section, House, Floor
from admin_messages.models import Message
from users.models import User


class MessageForm(forms.ModelForm):
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Тема сообщения:'}))
    text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'compose-textarea form-control', 'rows': '5',
                                     'placeholder': 'Текст сообщения:'}), required=False)
    house = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control select2-field'}), empty_label='',
                                   queryset=House.objects.all(), required=False)
    section = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control select2-field'}), empty_label='',
                                     queryset=Section.objects.all(), required=False)
    floor = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control select2-field'}), empty_label='',
                                   queryset=Floor.objects.all(), required=False)
    apartment = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control select2-field'}),
                                       empty_label='', required=False,
                                       queryset=Apartment.objects.all())
    owners_has_debt = forms.BooleanField(widget=forms.CheckboxInput(), required=False)

    receiver = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control select2-field'}),
                                      empty_label='', queryset=User.get_owners(), required=False)

    class Meta:
        model = Message
        fields = '__all__'
        exclude = ['receivers', 'sender', 'owners_has_debt', 'receiver']
