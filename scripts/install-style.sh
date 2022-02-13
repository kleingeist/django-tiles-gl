#!/bin/sh
set -e

SCRIPT=`realpath "$0"`
SCRIPT_PATH=`dirname "$SCRIPT"`
PROJECT_PATH=`dirname "$PROJECT_PATH"`
BUILD_PATH="$PROJECT_PATH/build"

APP_PATH="$PROJECT_PATH/django_tiles_gl"
APP_STATIC_PATH="$APP_PATH/static/django-tiles-gl"
APP_TEMPLATE_PATH="$APP_PATH/templates/django_tiles_gl"

SPRITES_PATH="$APP_STATIC_PATH/sprites"
FONTS_PATH="$APP_STATIC_PATH/fonts"

rm -rf "$SPRITES_PATH" || true
mkdir -p "$SPRITES_PATH"
cp "$BUILD_PATH/style/sprites/"* "$SPRITES_PATH"

rm -rf "$FONTS_PATH" || true
mkdir -p "$FONTS_PATH"
cp -r "$BUILD_PATH/fonts/_output/Open Sans"* "$FONTS_PATH"

mkdir -p "$APP_TEMPLATE_PATH"
cp "$BUILD_PATH/style/style-template.json" "$APP_TEMPLATE_PATH/style.json"
