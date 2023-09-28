from collections import defaultdict

from django.http import Http404
from django.shortcuts import redirect, render

from .forms import RequirementForm, UserStoryForm
from .models import Project, UserStory


def add_user_story(request, project_id):
    if request.method == 'POST':
        form = UserStoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_stories')
        else:
            raise Http404("Not valid")
    else:
        form = UserStoryForm()
        form.fields['project'].initial = Project.objects.get(id=project_id)
    max_ = 1
    try:
        max_ = UserStory.objects.filter(
            project_id=project_id).order_by('key').last().key
        max_ += 1
    except AttributeError:
        pass
    form.fields['key'].widget.attrs['min'] = max_
    form.fields['key'].widget.attrs['value'] = max_
    return render(request, 'add_user_story.html', {'form': form})


def add_requirement(request, project_id):
    if request.method == 'POST':
        sequence = []
        alt_sequence = defaultdict(list)
        for key, item in request.POST.items():
            if item and key.startswith('sequence'):
                sequence.append(item)
            if item and key.startswith('alt_sequence'):
                step = key.split('alt_sequence')[1].split('.')[0]
                alt_sequence[step].append(item)
        final_dict = request.POST.copy()
        final_dict['sequence'] = sequence
        final_dict['alt_sequence'] = alt_sequence
        form = RequirementForm(final_dict)
        if form.is_valid():
            form.save()
            return redirect('requirements')
        else:
            raise Http404("Not valid")
    else:
        form = RequirementForm()
        form.fields['project'].initial = Project.objects.get(id=project_id)
    return render(request, 'add_requirement.html', {'form': form})
