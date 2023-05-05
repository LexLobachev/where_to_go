from django.contrib import admin
from .models import Place, Image


class ImageInline(admin.StackedInline):
    model = Image
    exta = 0


@admin.register(Place)
class AdminPlace(admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ['title']


@admin.register(Image)
class AdminImage(admin.ModelAdmin):
    list_display = ['image']
