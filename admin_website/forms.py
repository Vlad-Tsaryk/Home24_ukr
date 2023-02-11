from django import forms
from django.forms import modelformset_factory

from admin_website.models import MainPage, Seo, Block


class MainPageForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    image1 = forms.ImageField(widget=forms.FileInput(), required=False)
    image2 = forms.ImageField(widget=forms.FileInput(), required=False)
    image3 = forms.ImageField(widget=forms.FileInput(), required=False)
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control compose-textarea', 'rows': '6'}),
                           required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = MainPage
        fields = '__all__'
        exclude = ['seo']


class SeoForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '6'}))
    keywords = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '6'}))

    class Meta:
        model = Seo
        fields = '__all__'


class BlockForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control compose-textarea', 'rows': '6'}),
                                  required=False)
    image = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = Block
        fields = '__all__'
        exclude = ['main_page']


BlockFormSet = modelformset_factory(Block, BlockForm, extra=0, max_num=6)
