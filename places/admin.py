from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin
from django.contrib import admin
from django.utils.html import format_html

from .models import Place, Image


class ImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Image
    exta = 0

    def get_place_image(self, place):
        return format_html('<img src="{}" height=200px />', place.image.url)

    readonly_fields = ['get_place_image']


@admin.register(Place)
class AdminPlace(SortableAdminBase, admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ['title']
    search_fields = ['title']


@admin.register(Image)
class AdminImage(admin.ModelAdmin):
    list_display = ['image']
