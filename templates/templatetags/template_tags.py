from django import template
register = template.Library()


def paginator(object):
    return {'object': object}


register.inclusion_tag('inc/paginator.html')(paginator)
