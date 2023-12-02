from django import template

register = template.Library()

@register.simple_tag
def note_tags_array(tag):
    return str(tag).split(',')



