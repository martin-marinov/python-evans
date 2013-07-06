from django import template
register = template.Library()


@register.filter
def classname(post):
    return post.__class__.__name__.lower()


@register.filter
def is_starred(post):
    return str(post.starred).lower()
