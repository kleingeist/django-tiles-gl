from django import template

register = template.Library()


@register.inclusion_tag("django_tiles_gl/maplibre_head.html")
def maplibre_head():
    return {}
