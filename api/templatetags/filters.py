from django import template

register = template.Library()


@register.filter
def get_dictionary_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def determine_article(user_input):
    if user_input.startswith(('a', 'e', 'i', 'o')):
        return 'an'
    else:
        return 'a'
