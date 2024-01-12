from django import template
from utils.breadcrumbs import generate_breadcrumbs

register = template.Library()


@register.simple_tag
def get_breadcrumbs(request):
    return generate_breadcrumbs(request)
