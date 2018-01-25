from django import template

from hub.models import SiteConfig

register = template.Library()


@register.simple_tag
def site_name(request):
    return SiteConfig.objects.get_or_create(pk=1)[0].name


@register.simple_tag
def site_current_release_version(request):
    return SiteConfig.objects.get_or_create(pk=1)[0].current_release_version


@register.simple_tag
def site_current_release_notes(request):
    current_release_notes = SiteConfig.objects.get_or_create(pk=1)[0].current_release_notes
    return current_release_notes.slug if current_release_notes is not None else None


@register.simple_tag
def site_custom_links(request):
    links = {}
    for link in SiteConfig.objects.get_or_create(pk=1)[0].custom_links.all():
        links[link.name] = link.url
    return links
