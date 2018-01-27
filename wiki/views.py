from django.shortcuts import render, get_object_or_404, redirect

from wiki.models import Entry, Section


def wiki(request):
    template_name = 'wiki/wiki_carousel.html'
    entries_per_section = {}
    wiki_sections = Section.objects.all()
    for section in wiki_sections:
        entries_per_section[section] = Entry.objects.filter(publish__exact=True, section__exact=section)
    return render(request, template_name, {'entries_per_section': entries_per_section})


def entry(request, entry_slug):
    template_name = 'wiki/wiki_entry.html'
    returned_entry = get_object_or_404(Entry, slug=entry_slug)
    entry_custom_fields_per_type = {}
    for custom_field_type in returned_entry.custom_fields_presentation_order.all():
        custom_fields_of_given_type = []
        for custom_field in returned_entry.custom_fields.all():
            if custom_field.type == custom_field_type:
                custom_fields_of_given_type.append(custom_field)
        entry_custom_fields_per_type[custom_field_type] = custom_fields_of_given_type
    return render(request, template_name,
                  {'entry': returned_entry, 'entry_custom_fields_per_type': entry_custom_fields_per_type,
                   'favorite_by': returned_entry.favorite_by.all()})


def add_entry_as_favorite(request, entry_slug):
    wiki_entry = Entry.objects.get(slug=entry_slug)
    wiki_entry.favorite_by.add(request.user)
    wiki_entry.save()
    return redirect('wiki_entry', entry_slug=entry_slug)


def remove_entry_as_favorite(request, entry_slug):
    wiki_entry = Entry.objects.get(slug=entry_slug)
    wiki_entry.favorite_by.remove(request.user)
    wiki_entry.save()
    return redirect('wiki_entry', entry_slug=entry_slug)
