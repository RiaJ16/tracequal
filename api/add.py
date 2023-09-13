from django.shortcuts import render


def add_user_story(request):
    if request.method == 'POST':
        print(request)
    else:
        return render(request, 'add_user_story.html')


def add_requirement(request):
    if request.method == 'POST':
        print(request)
    else:
        return render(request, 'add_requirement.html')
