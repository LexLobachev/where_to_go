from django.contrib import admin
from django.utils.html import format_html

from .models import Place, Image


class ImageInline(admin.StackedInline):
    model = Image
    exta = 0

    def get_place_images(self, object):
        return format_html(f'<img src="{object.image.url}" height=200px />')

    readonly_fields = ['get_place_images']


@admin.register(Place)
class AdminPlace(admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ['title']


@admin.register(Image)
class AdminImage(admin.ModelAdmin):
    list_display = ['image']
