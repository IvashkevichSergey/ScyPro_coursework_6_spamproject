from django import template

register = template.Library()


@register.simple_tag()
def process_media(url):
    if not url:
        return '/media/blog/no-foto.jpg'
    return url
