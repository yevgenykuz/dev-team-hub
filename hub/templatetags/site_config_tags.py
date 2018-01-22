from django import template
from hub.models import SiteConfig

register = template.Library()


@register.simple_tag
def site_name(request):
    return SiteConfig.objects.get_or_create(pk=1)[0].name


@register.simple_tag
def site_current_release_version(request):
    return SiteConfig.objects.get_or_create(pk=1)[0].current_release_version


@register.inclusion_tag("includes/custom_links_dropdown.html")
def site_custom_links(request):
    links = {}
    for link in SiteConfig.objects.get_or_create(pk=1)[0].custom_links.all():
        links[link.name] = link.url
    return links
