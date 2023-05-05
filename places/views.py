from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from places.models import Place


def index(request):
    places = []
    for place in Place.objects.all():
        place = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    place.lat,
                    place.lon
                ]
            },
            "properties": {
                "title": place.title,
                "placeId": place.pk,
                "detailsUrl": f"/static/places/roofs24.json"
            }
        }
        places.append(place)
    collection = {
        "type": "FeatureCollection",
        "features": places
    }
    return render(request, 'index.html', context={"geo_json": collection})


def get_place(request, id):
    place = get_object_or_404(Place, id=id)
    images_urls = [item.image.url for item in place.images.all()]
    response_data = {
        "title": place.title,
        "imgs": images_urls,
        "description_short": place.description_short,
        "description_long": place.description_long,
        "coordinates": {
            "lng": place.lat,
            "lat": place.lon,
        },
    }
    return JsonResponse(response_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2})
