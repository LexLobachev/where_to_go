from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description_short = models.TextField(blank=True, verbose_name="Короткое описание")
    description_long = HTMLField(verbose_name="Длинное описание")
    lat = models.FloatField(blank=True, verbose_name="широта")
    lon = models.FloatField(blank=True, verbose_name="долгота")

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.title


class Image(models.Model):
    place = models.ForeignKey('Place', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('Картинка', blank=True)
    position = models.IntegerField('Номер картинки', blank=True, default=0)

    class Meta:
        ordering = ['position']
