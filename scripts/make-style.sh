#!/bin/bash
set -e

STYLE_SRC="https://github.com/openmaptiles/osm-bright-gl-style/archive/refs/heads/master.tar.gz"

SCRIPT=`realpath "$0"`
SCRIPT_PATH=`dirname "$SCRIPT"`
PROJECT_PATH=`dirname "$PROJECT_PATH"`
BUILD_PATH="$PROJECT_PATH/build"
APP_PATH="$PROJECT_PATH/django_tiles_gl"

NODE_PATH="$PROJECT_PATH/node_modules"

STYLE_PATH="$BUILD_PATH/style"

rm -rf "$STYLE_PATH" || true
mkdir -p "$STYLE_PATH"

curl -sSL "$STYLE_SRC" | tar xvz -C "$STYLE_PATH" --strip-components=1

mkdir "$STYLE_PATH/sprites"
node "$SCRIPT_PATH/generate-sprites" "$STYLE_PATH/icons" "$STYLE_PATH/sprites"

STYLE_DATA=$(<"$STYLE_PATH/style.json")

STYLE_DATA=${STYLE_DATA//Noto Sans/Open Sans}

VECTOR_URL="https://api.maptiler.com/tiles/v3/tiles.json?key={key}"
VECTOR_URL_REPLACEMENT="{{ VECTOR_SOURCE_URL }}"
STYLE_DATA=${STYLE_DATA/$VECTOR_URL/$VECTOR_URL_REPLACEMENT}

SPRITE_URL="https://openmaptiles.github.io/osm-bright-gl-style/sprite"
SPRITE_URL_REPLACEMENT="{{ SPRITE_BASE_URL }}"
STYLE_DATA=${STYLE_DATA/$SPRITE_URL/$SPRITE_URL_REPLACEMENT}

GLYPH_URL="https://api.maptiler.com/fonts"
GLYPH_URL_REPLACEMENT="{{ GLYPH_BASE_URL }}"
STYLE_DATA=${STYLE_DATA/$GLYPH_URL/$GLYPH_URL_REPLACEMENT}

echo -n "$STYLE_DATA" > "$STYLE_PATH/style-template.json"
