def determine_article(user_input):
    if user_input.startswith(('a', 'e', 'i', 'o')):
        return 'an'
    else:
        return 'a'
