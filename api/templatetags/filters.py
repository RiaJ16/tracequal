from django import template

register = template.Library()


@register.filter
def get_dictionary_item(dictionary, key):
    try:
        return dictionary.get(str(key))
    except AttributeError:
        return None


@register.filter
def determine_article(user_input):
    if user_input.startswith(('a', 'e', 'i', 'o')):
        return 'an'
    else:
        return 'a'
