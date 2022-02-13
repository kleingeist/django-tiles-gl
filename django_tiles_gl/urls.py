from django.urls import path

from . import views

app_name = "django_tiles_gl"

urlpatterns = [
    path("<int:z>/<int:x>/<int:y>.pbf", views.tile, name="tile"),
    path(
        "style/openmaptiles.json", views.openmaptiles_style, name="openmaptiles_style"
    ),
    path("tiles.json", views.tilejson, name="tilejson"),
]
