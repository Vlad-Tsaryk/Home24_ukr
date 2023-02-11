from django.db import models


# Create your models here.
class SEO(models.Model):
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
    seo = models.OneToOneField(SEO, on_delete=models.PROTECT)


class Block(models.Model):
    title = models.CharField(max_length=70)
    description = models.TextField()
    image = models.ImageField()
    main_page = models.ForeignKey(MainPage, on_delete=models.CASCADE)
