# Django Tiles GL

Integrated Django Vector Tile Server based on mbtiles.


## Description

Simple app to serve [Mabpox Vector Tiles](https://docs.mapbox.com/data/tilesets/guides/vector-tiles-standards/) directly from [MBTiles files](https://github.com/mapbox/mbtiles-spec) via Django views.

Django Tiles has a minimal dependencies. It does not require GeoDjano or any other libraries. Its only dependency is Django itself.

Django Tiles GL **does not create raster tiles**. It may only be used with map libraries that support to render vector tiles like  [MapLibre](https://maplibre.org/) or [OpenLayers](https://openlayers.org/).

Django Tiles GL contains the [OSM Bright map style](https://openmaptiles.org/styles/#osm-bright) which can be used to render Vector Tiles following the [OpenMapTiles vector tile  schema](https://openmaptiles.org/schema).

Note that this default style is using [OpenSans fonts](https://github.com/openmaptiles/fonts) which does only contain Latin, Greek and Cyrillic alphabets.

Other tile schemes are possible by creating a custom [map style specification](https://docs.mapbox.com/mapbox-gl-js/style-spec/) and referencing Django Tiles GL [TileJSON endpoint](https://github.com/mapbox/tilejson-spec) as a source.

## Usage

See the [`demo`](https://github.com/kleingeist/django-tiles-gl/tree/main/demo) Django application for a simple usage example.


### Setup

- Add `django_tiles_gl` to you `INSTALLED_APPS` setting.
- Add `django_tiles_gl.urls` to your url patterns.
  For example with the `tiles` prefix:
  ```python
  urlpatterns = [
      ...
      path("tiles/", include("django_tiles_gl.urls")),
  ]
  ```
- Set path to your MBTiles files in you application settings.
  ```python
  MBTILES_DATABASE = BASE_DIR / "demo" / "data" / "berlin.mbtiles"
  ```
- Optionally set the default center to be set on the default map style.
  ```python
  MBTILES_CENTER = [13.4, 52.5, 13]   # [longitude, latitude, zoom]
  ```
- Force absolute urls to use SSL by prefixing them with "https://".
  This might be required if you app is running behind a reverse proxy and you
  are not able to set [`SECURE_PROXY_SSL_HEADER`](https://docs.djangoproject.com/en/4.0/ref/settings/#secure-proxy-ssl-header)
  from the SSL enabled proxy server.
  ```python
  MBTILES_FORCE_SSL = True
  ```

### Views
To render a map you have to include a JavaScript mapping library and refer to the `tile` endpoint or the default integrated style.

Django Tiles GL provides the following endpoints:

- `{% url 'django_tiles_gl:openmaptiles_style' %}` - Default [OpenMapTiles style defintion](https://openmaptiles.org) using the [OSM Bright map style](https://openmaptiles.org/styles/#osm-bright).
- `{% url 'django_tiles_gl:tilejson' %}` - [TileJSON](https://github.com/mapbox/tilejson-spec) describing the configured MBTiles files and providing the correct tile urls.
- `{% url 'django_tiles_gl:tile' x y z %}` - Actual tile endpoint, returning vector data in the [PBF format](https://wiki.openstreetmap.org/wiki/PBF_Format).


Django Tiles GL is bundles with [MapLibre](https://maplibre.org/) and provides a template tag for easy inclusion. A minimal working example has to contain the following defintions:

```html
{% load tiles_gl_tags %}
<!DOCTYPE html>
<html>
<head>
    {% maplibre_head %}

    <style>
        body { margin:0; padding:0; }
        #map { position:absolute; top:0; bottom:0; width:100%; }
    </style>
</head>
<body>

<div id='map'></div>

<script>
var map = new maplibregl.Map({
	container: 'map',
	style: '{% url 'django_tiles_gl:openmaptiles_style' %}',
});
</script>

</body>
</html>
```

## Data / MBTiles generation

There are mutiple tools to generate valid MBTiles databases. The easiest to use with Django Tiles GL is [OpenMapTiles](https://github.com/openmaptiles/openmaptiles) as it is compatible with the bundled default style.

For a quickstart you may generate the MbTiles for an area with the following commands:
```sh
git clone https://github.com/openmaptiles/openmaptiles.git
cd openmaptiles
./quickstart.sh <area>
```

Fo further information and optiones see [https://github.com/openmaptiles/openmaptiles](https://github.com/openmaptiles/openmaptiles)



## Further Topics

### Caching

It is advised setup a caching proxy for the `tile` endpoint. Please refer to you HTTP servers documentation. For example the [nginx proxy cache config](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cache)



## Other Django tile server solutions

- [django-geojson-tiles](https://github.com/glenrobertson/django-geojson-tiles) - Generates GeoJSON tiles from a GeoDjango model. No MBTiles support.  Not to be used as a base layer.

- [django-vectortiles](https://github.com/submarcos/django-vectortiles) - Generates Vector Tile layers from GeoDjango. No MBTiles support. Not to be used as a base layer.

- [django-mbtiles](https://github.com/makinacorpus/django-mbtiles) - Uses MBTiles to generate rastered tiles and [UTFGrid](https://github.com/mapbox/mbtiles-spec/blob/master/1.1/utfgrid.md). Does not support modern vector tiles. Strong inspiration for this project.
