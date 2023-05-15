from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from places.models import Place


def index(request):
    features = []
    places = Place.objects.all()

    for place in places:
        place = {
            'type': 'Feature',

            'geometry': {
                'type': 'Point',
                'coordinates': [
                    place.lat,
                    place.lon
                ]
            },

            'properties': {
                'title': place.title,
                'placeId': place.id,
                'detailsUrl': reverse('places', args={place.id})
            }
        }
        features.append(place)

    collection = {
        'type': 'FeatureCollection',
        'features': features
    }

    return render(request, 'index.html', context={'geo_json': collection})


def get_place(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    images_urls = [item.image.url for item in place.images.all()]
    response_data = {
        'title': place.title,
        'imgs': images_urls,
        'description_short': place.description_short,
        'description_long': place.description_long,
        'coordinates': {
            'lng': place.lat,
            'lat': place.lon,
        },
    }
    return JsonResponse(response_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2})
