from django.http import Http404
from django.shortcuts import redirect, render

from .forms import UserStoryForm
from .models import Project, UserStory


def edit_user_story(request, project_id, us_id):
    if request.method == 'POST':
        us = UserStory.objects.get(id=us_id)
        form = UserStoryForm(request.POST, instance=us)
        if form.is_valid():
            form.save()
            print(form.__dict__)
            return redirect('user_stories')
        else:
            raise Http404("Not valid")
    else:
        us = UserStory.objects.get(id=us_id, project_id=project_id)
        form = UserStoryForm(instance=us)
        data = {'form': form, 'user_story': us}
    return render(request, 'edit_user_story.html', data)
