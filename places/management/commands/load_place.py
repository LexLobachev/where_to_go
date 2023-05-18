import logging
import time

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from places.models import Image, Place


def load_place(place_url):
    response = requests.get(place_url, allow_redirects=True)
    response.raise_for_status()
    raw_place = response.json()
    place, created = Place.objects.get_or_create(
        title=raw_place['title'],
        defaults={
            'description_short': raw_place.get('description_short', ''),
            'description_lon': raw_place.get('description_long', ''),
            'lat': raw_place['coordinates']['lng'],
            'lon': raw_place['coordinates']['lat']
        }
    )

    for index, img in enumerate(raw_place.get('imgs', []), 1):
        response = requests.get(img)
        response.raise_for_status()
        Image.objects.get_or_create(
            place=place,
            image=ContentFile(response.content, name=f'image{index}.jpeg'),
            defaults={
                'position': index
            }
        )


class Command(BaseCommand):
    help = 'Load Places'

    def add_arguments(self, parser):
        parser.add_argument('-url', '--load_url', nargs='?', help="Enter url with pace's json")

    def handle(self, *args, **options):
        place_url = options['load_url']
        try:
            load_place(place_url)
        except requests.exceptions.ConnectionError:
            logging.error('No internet')
        except (requests.exceptions.HTTPError, requests.exceptions.JSONDecodeError) as err:
            logging.error(f'Something went wrong {err}')
