#!/bin/sh
set -e

FONT_SRC="https://github.com/openmaptiles/fonts/archive/refs/heads/master.tar.gz"

SCRIPT=`realpath "$0"`
SCRIPT_PATH=`dirname "$SCRIPT"`
PROJECT_PATH=`dirname "$PROJECT_PATH"`
BUILD_PATH="$PROJECT_PATH/build"
NODE_PATH="$PROJECT_PATH/node_modules"

FONT_PATH="$BUILD_PATH/fonts"

rm -rf "$FONT_PATH" || true
mkdir -p "$FONT_PATH"
cd $FONT_PATH

curl -sSL "$FONT_SRC" | tar xvz --strip-components=1
node generate.js