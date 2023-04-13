#!/bin/sh
set -e

SCRIPT=`realpath "$0"`
SCRIPT_PATH=`dirname "$SCRIPT"`
PROJECT_PATH=`dirname "$PROJECT_PATH"`

APP_PATH="$PROJECT_PATH/django_tiles_gl"
APP_STATIC_PATH="$APP_PATH/static/django-tiles-gl"

MAPLIBRE_DIST_PATH="$PROJECT_PATH/node_modules/maplibre-gl/dist"
MAPLIBRE_PATH="$APP_STATIC_PATH/maplibre"

rm -rf "$MAPLIBRE_PATH" || true
mkdir -p "$MAPLIBRE_PATH"
curl -sSL "https://raw.githubusercontent.com/maplibre/maplibre-gl-js/main/LICENSE.txt" > "$MAPLIBRE_PATH/LICENSE.txt"
cp "$MAPLIBRE_DIST_PATH/maplibre-gl.css" "$MAPLIBRE_PATH"
cp "$MAPLIBRE_DIST_PATH/maplibre-gl.js" "$MAPLIBRE_PATH"

# Remove unused sourceMappingURL defintion that may result in collectstatic errors
sed -i '/^\/\/# sourceMappingURL/d' "$MAPLIBRE_PATH/maplibre-gl.js"
