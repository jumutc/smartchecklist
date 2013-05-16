# coding=utf-8
from django.contrib.humanize.templatetags.humanize import intcomma
from django import template

register = template.Library()

@register.filter
def currency(value, arg):
    value = round(float(value), 2)
    return "%s%s%s" % (arg, intcomma(int(value)), ("%0.2f" % value)[-3:])
