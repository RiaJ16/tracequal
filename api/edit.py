from django.http import Http404
from django.shortcuts import redirect, render

from .common import dict_with_sequences
from .forms import DesignForm, RequirementForm, UserStoryForm
from .models import Design, Requirement, UserStory


def edit_user_story(request, project_id, us_id):
    if request.method == 'POST':
        us = UserStory.objects.get(id=us_id)
        form = UserStoryForm(request.POST, instance=us)
        if form.is_valid():
            form.save()
            return redirect('user_stories')
        else:
            raise Http404("Not valid")
    else:
        us = UserStory.objects.get(id=us_id, project_id=project_id)
        form = UserStoryForm(instance=us)
        data = {'form': form, 'user_story': us}
    return render(request, 'edit_user_story.html', data)


def edit_requirement(request, project_id, id):
    if request.method == 'POST':
        requirement = Requirement.objects.get(id=id, project_id=project_id)
        form = RequirementForm(
            dict_with_sequences(request.POST), instance=requirement)
        if form.is_valid():
            form.save()
            return redirect('requirements')
        else:
            raise Http404("Not valid")
    else:
        requirement = Requirement.objects.get(id=id, project_id=project_id)
        form = RequirementForm(instance=requirement)
        data = {'form': form, 'requirement': requirement}
    return render(request, 'edit_requirement.html', data)


def edit_design(request, project_id, design_id):
    if request.method == 'POST':
        design = Design.objects.get(id=design_id)
        form = DesignForm(request.POST, request.FILES, instance=design)
        if form.is_valid():
            form.save()
            return redirect('design')
        else:
            raise Http404("Not valid")
    else:
        design = Design.objects.get(id=design_id, project_id=project_id)
        form = DesignForm(instance=design)
        data = {'form': form, 'design': design}
    return render(request, 'edit_design.html', data)
