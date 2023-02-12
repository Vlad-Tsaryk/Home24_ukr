import io
import os

from PIL import Image
from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import FileExtensionValidator
from django.forms import modelformset_factory

from admin_website.models import MainPage, Seo, Block, ContactPage, ServicePage, ServiceBlock, TariffPage, TariffBlock, \
    AboutPage, Document, Gallery, AdditionalGallery


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
        self.fields['text'].widget.attrs['class'] = 'form-control compose-textarea'

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


class AboutPageForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control compose-textarea', 'rows': '6'}),
                           required=False)
    photo = forms.ImageField(widget=forms.FileInput(), required=False,
                             error_messages={'invalid_image': 'К загрузке поддерживаются только изображения'})
    additional_title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    additional_text = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control compose-textarea', 'rows': '6'}), required=False)

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            try:
                original_format = photo.content_type.split('/')[-1]
                with io.BytesIO(photo.read()) as f:
                    img = Image.open(f)
                    if img.size != (250, 310):
                        img.thumbnail((250, 310))
                    output = io.BytesIO()
                    img.save(output, format=original_format)
                    output.seek(0)
                    return InMemoryUploadedFile(output, 'ImageField', photo.name,
                                                f'image/{original_format}', output.getbuffer().nbytes, None)
            except:
                return photo

    class Meta:
        model = AboutPage
        fields = '__all__'
        exclude = ['seo', ]


class DocumentForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    file = forms.FileField(widget=forms.FileInput(attrs={'accept': '.pdf, .jpg'}),
                           validators=[FileExtensionValidator(allowed_extensions=["pdf", "jpg"],
                                                              message='Только файлы c расширением PDF и JPG')])

    # def clean_file(self):
    #     file = self.cleaned_data.get('file')
    #     if file:
    #         try:
    #             with io.BytesIO(file.read()) as f:
    #                 img = Image.open(f)
    #                 if img.size != (32, 42):
    #                     img = img.resize((32, 42))
    #                 output = io.BytesIO()
    #                 img.save(output, format='JPEG')
    #                 output.seek(0)
    #                 return InMemoryUploadedFile(output, 'ImageField', file.name,
    #                                             'image/jpeg', output.getbuffer().nbytes, None)
    #         except OSError:
    #             return file

    class Meta:
        model = Document
        fields = '__all__'
        exclude = ['about_page', ]


DocumentFormSet = modelformset_factory(Document, DocumentForm, extra=0, can_delete=True)


class GalleryForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(), required=False,
                             error_messages={'invalid_image': 'К загрузке поддерживаются только изображения'})

    class Meta:
        model = Gallery
        fields = '__all__'
        exclude = ['about_page', ]


class AdditionalGalleryForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(), required=False,
                             error_messages={'invalid_image': 'К загрузке поддерживаются только изображения'})

    class Meta:
        model = AdditionalGallery
        fields = '__all__'
        exclude = ['about_page', ]
