from django.urls import path

from . import views

urlpatterns = [
    path("<int:z>/<int:x>/<int:y>.pbf", views.tile, name="tile"),
    path("style/openmaptiles.json", views.openmaptiles_style),
    path("tiles.json", views.tilejson, name="tilejson"),
]
