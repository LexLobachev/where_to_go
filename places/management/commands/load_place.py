import logging
import time

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from places.models import Image, Place


def load_place(place_url):
    response = requests.get(place_url, allow_redirects=True)
    response.raise_for_status()
    place_json = response.json()
    place, created = Place.objects.get_or_create(
        title=place_json['title'],
        defaults={
            'description_short': place_json['description_short'],
            'description_lon': place_json['description_long'],
            'lat': place_json['coordinates']['lng'],
            'lon': place_json['coordinates']['lat']
        }
    )

    for index, img in enumerate(place_json['imgs'], 1):
        response = requests.get(img)
        response.raise_for_status()
        Image.objects.get_or_create(
            place=place,
            position=index,
            defaults={
                'image': ContentFile(response.content, name=f'image{index}.jpeg')
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
            logging.error('No internet, will try to reconnect in 10 seconds')
            time.sleep(10)
        except requests.exceptions.HTTPError as err:
            logging.error(f'Something went wrong {err}')
        except requests.exceptions.JSONDecodeError as err:
            logging.error(f'Something went wrong {err}')
