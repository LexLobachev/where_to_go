from django.db import models


class Place(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description_short = models.TextField(blank=True, verbose_name="Короткое описание")
    description_long = models.TextField(blank=True, verbose_name="Длинное описание")
    lat = models.FloatField(blank=True, verbose_name="широта")
    lon = models.FloatField(blank=True, verbose_name="долгота")

    def __str__(self):
        return self.title


class Image(models.Model):
    place = models.ForeignKey('Place', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('Картинка', blank=True)
