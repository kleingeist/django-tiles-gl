import json
from importlib.metadata import metadata
from pathlib import Path

from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.cache import cache_control

from .mbtiles import MissingTileError, open_mbtiles
from .utils import center_from_bounds, build_absolute_uri

DEFAULT_ZOOM = 13
DEFAULT_MINZOOM = 7
DEFAULT_MAXZOOM = 15
WORLD_BOUNDS = [-180, -85.05112877980659, 180, 85.0511287798066]

MONTH_SECONDS = 60 * 60 * 24 * 30


@cache_control(max_age=MONTH_SECONDS)
def tile(request, z, x, y):
    with (open_mbtiles()) as mbtiles:
        try:
            data = mbtiles.tile(z, x, y)
            response = HttpResponse(
                content=data,
                status=200,
            )
            response["Content-Type"] = "application/x-protobuf"
            response["Content-Encoding"] = "gzip"

            return response

        except MissingTileError:
            return HttpResponse(
                status=204,
            )


def openmaptiles_style(request):
    if hasattr(settings, "MBTILES_CENTER"):
        center = settings.MBTILES_CENTER
    else:
        with open_mbtiles() as mbtiles:
            metadata = mbtiles.metadata()
            bounds = metadata.get("bounds", WORLD_BOUNDS)
            center = metadata.get("center", center_from_bounds(bounds, DEFAULT_ZOOM))

    base_url = staticfiles_storage.url("django-tiles-gl/")
    if not base_url.startswith("http"):
        base_url = build_absolute_uri(request, base_url)

    tilejson_url = build_absolute_uri(request, reverse("django_tiles_gl:tilejson"))

    app_path = Path(__file__).parent
    style_json_path = app_path / "templates" / "django_tiles_gl" / "style.json"
    with style_json_path.open() as f:
        style = json.load(f)

    style["center"] = [center[0], center[1]]
    style["zoom"] = center[2]
    style["sprite"] = base_url + "sprites/sprite"
    style["glyphs"] = base_url + r"fonts/{fontstack}/{range}.pbf"
    style["sources"] = {"openmaptiles": {"type": "vector", "url": tilejson_url}}

    return JsonResponse(style)


def tilejson(request):
    with open_mbtiles() as mbtiles:
        metadata = mbtiles.metadata()

        # Load valid tilejson keys from the mbtiles metadata
        valid_tilejson_keys = (
            # MUST
            "name",
            "format",
            # SHOULD
            "bounds",
            "center",
            "minzoom",
            "maxzoom",
            # MAY
            "attribution",
            "description",
            "type",
            "version",
            # UNSPECIFIED
            "scheme",
        )
        spec = {key: metadata[key] for key in valid_tilejson_keys if key in metadata}

        if spec["format"] == "pbf":
            spec["vector_layers"] = metadata["json"]["vector_layers"]
        else:
            raise NotImplementedError(
                f"Only mbtiles in pbf format are supported. Found {spec['format']}"
            )

        # Optional fields
        spec["scheme"] = spec.get("scheme", "xyz")
        spec["bounds"] = spec.get("bounds", WORLD_BOUNDS)
        spec["minzoom"] = spec.get("minzoom", DEFAULT_MINZOOM)
        spec["maxzoom"] = spec.get("maxzoom", DEFAULT_MINZOOM)
        spec["center"] = spec.get(
            "center", center_from_bounds(spec["bounds"], DEFAULT_ZOOM)
        )

        # Tile defintions
        tile_url = build_absolute_uri(
            request,
            reverse("django_tiles_gl:tile", args=(0, 0, 0))
        )
        tile_url = tile_url.replace("/0/0/0.pbf", r"/{z}/{x}/{y}.pbf")
        spec["tiles"] = [tile_url]

        # Version defintion
        spec["tilejson"] = "3.0.0"

        return JsonResponse(spec)
