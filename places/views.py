from django.shortcuts import render

from places.models import Place


def index(request):
    places = []
    for place in Place.objects.all():
        place = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    place.lon,
                    place.lat
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
    print(collection)
    return render(request, 'index.html', context={"geo_json": collection})
