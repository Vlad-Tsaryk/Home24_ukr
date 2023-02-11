from django import forms
from admin_website.models import MainPage


class MainPageForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = MainPage
        fields = '__all__'
