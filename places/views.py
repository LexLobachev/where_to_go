from django.shortcuts import render, get_object_or_404

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
    return render(request, 'places.html', context={'place': place})
