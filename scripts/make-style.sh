#!/bin/sh
set -e

STYLE_SRC="https://github.com/openmaptiles/osm-bright-gl-style/archive/refs/heads/master.tar.gz"

SCRIPT=`realpath "$0"`
SCRIPT_PATH=`dirname "$SCRIPT"`
PROJECT_PATH=`dirname "$PROJECT_PATH"`
BUILD_PATH="$PROJECT_PATH/build"
APP_PATH="$PROJECT_PATH/django_tiles_gl"

STYLE_PATH="$BUILD_PATH/style"

rm -rf "$STYLE_PATH" || true
mkdir -p "$STYLE_PATH"

curl -sSL "$STYLE_SRC" | tar xvz -C "$STYLE_PATH" --strip-components=1

mkdir "$STYLE_PATH/sprites"
node "$SCRIPT_PATH/generate-sprites.js" "$STYLE_PATH/icons" "$STYLE_PATH/sprites"

sed "s/Noto Sans/Open Sans/g" "$STYLE_PATH/style.json" > "$STYLE_PATH/style-template.json"
