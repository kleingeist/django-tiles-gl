
from importlib.metadata import metadata
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.urls import reverse
from django.shortcuts import render

from .mbtiles import MissingTileError, open_mbtiles
from django.contrib.staticfiles.storage import staticfiles_storage

default_zoom = 13
world_bounds = [-85.0511, -180.0, 85.0511, 180.0]

def tile(request, z, x, y):
    with (open_mbtiles()) as mbtiles:
        try:
            data = mbtiles.tile(z, x, y)
            return HttpResponse(
                content=data,
                headers={
                    "Content-Type": "application/x-protobuf",
                    "Content-Encoding": "gzip",
                },
                status=200,
            )

        except MissingTileError:
            return HttpResponse(
                status=204,
            )

def _center_from_bounds(bounds):
    return  [ (bounds[0] + bounds[2]) / 2.0, (bounds[1] + bounds[3]) / 2.0, ]


def openmaptiles_style(request):
    with open_mbtiles() as mbtiles:
        metadata = mbtiles.metadata()

    bounds = metadata.get("bounds")
    if bounds:
        bounds = [float(coord.strip()) for coord in bounds.split(",")]
    else: 
        bounds = world_bounds


    center = metadata.get("center")
    if center:
        center = [float(coord.strip()) for coord in center.split(",")]
    else:
        center = _center_from_bounds(bounds)

    base_url = staticfiles_storage.url("django-tiles-gl")
    if not base_url.startswith("http"):
        base_url = request.build_absolute_uri(base_url)

    sprite_base_url = f"{base_url}/sprites/sprite"
    glyph_base_url = f"{base_url}/fonts"
    vector_source_url = request.build_absolute_uri(reverse("tilejson"))
    return render(
        request, 
        "django_tiles_gl/style.json",
        {
            "VECTOR_SOURCE_URL": vector_source_url,
            "SPRITE_BASE_URL": sprite_base_url,
            "GLYPH_BASE_URL": glyph_base_url,
            "CENTER_LAT": center[1],
            "CENTER_LON": center[0],
            "ZOOM": default_zoom,
        },
        content_type="application/json")

def tilejson(request):
    with open_mbtiles() as mbtiles:
        metadata = mbtiles.metadata()

        bounds = metadata.get("bounds")
        if bounds:
            bounds = [float(coord.strip()) for coord in bounds.split(",")]
        else: 
            bounds = world_bounds

        center = metadata.get("center")
        if center:
            center = [float(coord.strip()) for coord in center.split(",")]
        else:
            (lon, lat) = _center_from_bounds(bounds)
            center = [ lon, lat, default_zoom]

        tile_url = request.build_absolute_uri(reverse("tile", args = (0, 0, 0)))
        tile_url = tile_url.replace("/0/0/0.pbf", "/{z}/{x}/{y}.pbf")

        spec = {
            "tilejson": "2.1.0",
            "name": metadata.get("name", "FIXME"),
            "description": metadata.get("description", "FIXME"),
            "version": metadata.get("version", "0.0.1"),
            "scheme": "xyz",
            "minzoom": int(metadata.get("minzoom", 0)),
            "maxzoom": int(metadata.get("maxzoom", 0)),
            "bounds": bounds,
            "center": center,
            "tiles": [ tile_url ],
            "format": "pbf",
        }

        if "attribution" in metadata:
            spec["attribution"] = metadata["attribution"]

        return JsonResponse(spec)
