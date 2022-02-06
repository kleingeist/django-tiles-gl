#!/bin/sh
set -e

SCRIPT=`realpath "$0"`
SCRIPT_PATH=`dirname "$SCRIPT"`
PROJECT_PATH=`dirname "$PROJECT_PATH"`
BUILD_PATH="$PROJECT_PATH/build"

APP_PATH="$PROJECT_PATH/django_tiles_gl"
APP_STATIC_PATH="$APP_PATH/static/django-tiles-gl"
APP_TEMPLATE_PATH="$APP_PATH/templates/django_tiles_gl"

rm -rf "$APP_STATIC_PATH" || true
mkdir -p "$APP_STATIC_PATH"

mkdir "$APP_STATIC_PATH/sprites"
cp "$BUILD_PATH/style/sprites/"* "$APP_STATIC_PATH/sprites/"
cp "$BUILD_PATH/style/style-template.json" "$APP_TEMPLATE_PATH/style.json"

mkdir "$APP_STATIC_PATH/fonts"
cp -r "$BUILD_PATH/fonts/_output/Open Sans"* "$APP_STATIC_PATH/fonts/"

