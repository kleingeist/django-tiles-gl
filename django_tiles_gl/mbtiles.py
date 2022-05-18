import json
import os
import sqlite3
from curses import meta

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from .utils import split_floats


class MissingTileError(Exception):
    pass


class MBTilesNotFoundError(Exception):
    pass


class MBTilesInvalid(Exception):
    pass


def open_mbtiles():
    database = getattr(settings, "MBTILES_DATABASE")
    if not database:
        raise ImproperlyConfigured("The MBTILES_DATABASE setting must not be empty.")
    return MBTiles(str(database))


class MBTiles:
    _connection = None

    def __init__(self, database):
        self._database = database

    def connect(self):
        if not os.path.exists(self._database):
            raise MBTilesNotFoundError(f"MBTiles database {self._database} does not exist")

        self._connection = sqlite3.connect(
            database=self._database,
            timeout=1.0,
            detect_types=0,
            isolation_level=None,
            check_same_thread=False,
        )

    def close(self):
        if self._connection:
            self._connection.close()
            self._connection = None

    def metadata(self):
        cursor = self._connection.cursor()
        cursor.execute("SELECT name, value FROM metadata")
        metadata = {row[0]: row[1] for row in cursor}
        cursor.close()

        self._validate_metadata(metadata)
        self._parse_metadata_bounds(metadata)
        self._parse_metadata_center(metadata)
        self._parse_metadata_zoom(metadata)
        self._parse_metadata_json(metadata)

        self._add_scheme_with_default(metadata)

        return metadata

    def _validate_metadata(self, metadata):
        required = ["name", "format"]
        for field in required:
            if field not in metadata:
                raise MBTilesInvalid(f'Missing required metadata field "{field}"')

        if metadata["format"] == "pbf":
            if "json" not in metadata:
                raise MBTilesInvalid(f'Missing required metadata field "json"')

    def _parse_metadata_bounds(self, metadata):
        if "bounds" in metadata:
            metadata["bounds"] = split_floats(metadata["bounds"])

    def _parse_metadata_center(self, metadata):
        if "center" in metadata:
            metadata["center"] = split_floats(metadata["center"])

    def _parse_metadata_zoom(self, metadata):
        for zoom in ("minzoom", "maxzoom"):
            if zoom in metadata:
                metadata[zoom] = float(metadata[zoom])

    def _parse_metadata_json(self, metadata):
        if "json" in metadata:
            metadata["json"] = json.loads(metadata["json"])

    # FIXME: WHAT SHOULD BE THE DEFAULT?
    def _add_scheme_with_default(self, metadata, default="tms"):
        metadata["scheme"] = metadata.get("scheme", default)

    # def _flip_y(self, y, z):
    #     return 2**z - 1 - y

    def tile(self, z, x, y):
        cursor = self._connection.cursor()
        # tms_y = self._flip_y(y, z)
        cursor.execute(
            "SELECT tile_data FROM tiles WHERE zoom_level=? AND tile_column=? AND tile_row=?;",
            # (z, x, tms_y),
            (z, x, y),
        )
        tile = cursor.fetchone()
        cursor.close()

        if not tile:
            raise MissingTileError()
        return tile

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()
