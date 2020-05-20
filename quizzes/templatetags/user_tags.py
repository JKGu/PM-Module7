from __future__ import unicode_literals
from django import template
from django.template.defaulttags import register


# register = template.Library()

@register.filter('has_group')
def has_group(user, group_name):

    groups = user.groups.all().values_list('name', flat=True)
    return True if group_name in groups else False

@register.filter('lookup')
def lookup(value, arg):
    return value[arg]


@register.filter('call_method')
def call_method(method, arg):
    return arg in list(method.values_list('name',flat=True))

@register.filter('get_score')
def get_score(method, arg):
    print(method)
    return method[str(arg)]
