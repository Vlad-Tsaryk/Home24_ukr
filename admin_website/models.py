from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Seo(models.Model):
    title = models.CharField(max_length=70)
    description = models.TextField()
    keywords = models.TextField()


# Create your models here.
class MainPage(models.Model):
    image1 = models.ImageField(upload_to='website/main_page')
    image2 = models.ImageField(upload_to='website/main_page')
    image3 = models.ImageField(upload_to='website/main_page')
    text = models.TextField()
    title = models.CharField(max_length=70)
    show_app_urls = models.BooleanField(default=True)
    seo = models.OneToOneField(Seo, on_delete=models.PROTECT)


class Block(models.Model):
    title = models.CharField(max_length=70)
    description = models.TextField()
    image = models.ImageField(upload_to='website/main_page/blocks')
    main_page = models.ForeignKey(MainPage, on_delete=models.CASCADE)


class ContactPage(models.Model):
    title = models.CharField(max_length=70)
    text = models.TextField()
    site_url = models.URLField()
    full_name = models.CharField(max_length=70)
    location = models.CharField(max_length=70)
    address = models.CharField(max_length=70)
    phone = PhoneNumberField()
    email = models.EmailField()
    map_code = models.TextField()
    seo = models.OneToOneField(Seo, on_delete=models.PROTECT)


class ServicePage(models.Model):
    seo = models.OneToOneField(Seo, on_delete=models.PROTECT)


class ServiceBlock(models.Model):
    image = models.ImageField(upload_to='website/service_page/blocks')
    title = models.CharField(max_length=70)
    text = models.TextField()
    service_page = models.ForeignKey(ServicePage, on_delete=models.CASCADE)


class TariffPage(models.Model):
    title = models.CharField(max_length=70)
    text = models.TextField()
    seo = models.OneToOneField(Seo, on_delete=models.PROTECT)


class TariffBlock(models.Model):
    image = models.ImageField(upload_to='website/tariff_page/blocks')
    title = models.CharField(max_length=70)
    tariff_page = models.ForeignKey(TariffPage, on_delete=models.CASCADE)


class AboutPage(models.Model):
    title = models.CharField(max_length=70)
    text = models.TextField()
    photo = models.ImageField(upload_to='website/about_page')
    additional_title = models.CharField(max_length=70)
    additional_text = models.TextField()
    seo = models.OneToOneField(Seo, on_delete=models.PROTECT)


class Document(models.Model):
    about_page = models.ForeignKey(AboutPage, on_delete=models.CASCADE)
    file = models.FileField(upload_to='website/about_page/documents')
    title = models.CharField(max_length=70)


class Gallery(models.Model):
    about_page = models.ForeignKey(AboutPage, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='website/about_page/gallery')


class AdditionalGallery(models.Model):
    about_page = models.ForeignKey(AboutPage, on_delete=models.CASCADE)
    image = models.FileField(upload_to='website/about_page/additional_gallery')
