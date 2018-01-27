from django import template

register = template.Library()


@register.filter()
def as_percentage(number):
    return "{:.2%}".format(number)
