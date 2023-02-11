from django import forms
from django.forms import modelformset_factory

from admin_website.models import MainPage, Seo, Block, ContactPage, ServicePage, ServiceBlock, TariffPage, TariffBlock


class MainPageForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    image1 = forms.ImageField(widget=forms.FileInput(), required=False,
                              error_messages={'invalid_image': 'К загрузке поддерживаются только изображения'})
    image2 = forms.ImageField(widget=forms.FileInput(), required=False,
                              error_messages={'invalid_image': 'К загрузке поддерживаются только изображения'})
    image3 = forms.ImageField(widget=forms.FileInput(), required=False,
                              error_messages={'invalid_image': 'К загрузке поддерживаются только изображения'})
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
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}), required=False,
                             error_messages={'invalid_image': 'К загрузке поддерживаются только изображения'})

    class Meta:
        model = Block
        fields = '__all__'
        exclude = ['main_page']


BlockFormSet = modelformset_factory(Block, BlockForm, extra=0, max_num=6)


class ContactPageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ContactPageForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ContactPage
        fields = '__all__'
        exclude = ['seo']


class ServicePageForm(forms.ModelForm):
    class Meta:
        model = ServicePage
        fields = '__all__'
        exclude = ['seo', ]


class ServiceBlockForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control compose-textarea', 'rows': '6'}),
                           required=False)
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}), required=False,
                             error_messages={'invalid_image': 'К загрузке поддерживаются только изображения'})

    class Meta:
        model = ServiceBlock
        fields = '__all__'
        exclude = ['service_page', ]


ServiceBlockFormSet = modelformset_factory(ServiceBlock, ServiceBlockForm, extra=0, can_delete=True)


class TariffPageForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control compose-textarea', 'rows': '6'}),
                           required=False)

    class Meta:
        model = TariffPage
        fields = '__all__'
        exclude = ['seo', ]


class TariffBlockForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}), required=False,
                             error_messages={'invalid_image': 'К загрузке поддерживаются только изображения'})

    class Meta:
        model = TariffBlock
        fields = '__all__'
        exclude = ['tariff_page', ]


TariffBlockFormSet = modelformset_factory(TariffBlock, TariffBlockForm, extra=0, can_delete=True)
