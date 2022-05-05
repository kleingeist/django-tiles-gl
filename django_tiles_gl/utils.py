from django.conf import settings


def split_floats(input, sep=","):
    return [float(val.strip()) for val in input.split(sep)]

def center_from_bounds(bounds, zoom):
    return [(bounds[0] + bounds[2]) / 2.0, (bounds[1] + bounds[3]) / 2.0, zoom]

def build_absolute_uri(request, location=None):
    uri = request.build_absolute_uri(location)

    if getattr(settings, "MBTILES_FORCE_SSL", False) and uri[:7].lower() == "http://":
        uri = "https://" + uri[7:]

    return uri
