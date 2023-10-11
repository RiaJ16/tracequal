from django.http import Http404
from django.shortcuts import redirect, render

from .common import dict_with_sequences
from .forms import (CodeForm, DesignForm, OptionsForm, ProjectForm,
                    RequirementForm, TestForm, UserStoryForm)
from .models import (Code, Design, Progress, Project, Requirement, Test,
                     UserStory)


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
    set_current_key(form, UserStory, project_id)
    return render(request, 'add_user_story.html', {'form': form})


def add_requirement(request, project_id):
    if request.method == 'POST':
        form = RequirementForm(dict_with_sequences(request.POST))
        if form.is_valid():
            form.save()
            return redirect('requirements')
        else:
            raise Http404("Not valid")
    else:
        form = RequirementForm()
        form.fields['project'].initial = Project.objects.get(id=project_id)
    set_current_key(form, Requirement, project_id)
    return render(request, 'add_requirement.html', {'form': form})


def add_design(request, project_id):
    if request.method == 'POST':
        form = DesignForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('design')
        else:
            raise Http404("Not valid")
    else:
        form = DesignForm()
        form.fields['project'].initial = Project.objects.get(id=project_id)
    set_current_key(form, Design, project_id)
    return render(request, 'add_design.html', {'form': form})


def add_code(request, project_id):
    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('code')
        else:
            raise Http404("Not valid")
    else:
        form = CodeForm()
        form.fields['project'].initial = Project.objects.get(id=project_id)
    set_current_key(form, Code, project_id)
    return render(request, 'add_code.html', {'form': form})


def add_test(request, project_id):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tests')
        else:
            raise Http404('Not valid')
    else:
        form = TestForm()
        form.fields['project'].initial = Project.objects.get(id=project_id)
    set_current_key(form, Test, project_id)
    return render(request, 'add_test.html', {'form': form})


def add_test_application(request, project_id):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tests')
        else:
            raise Http404('Not valid')
    else:
        form = TestForm()
        form.fields['project'].initial = Project.objects.get(id=project_id)
    set_current_key(form, Test, project_id)
    return render(request, 'add_test.html', {'form': form})


def set_current_key(form, model, project_id):
    max_ = 1
    try:
        max_ = model.objects.filter(
            project_id=project_id).order_by('key').last().key
        max_ += 1
    except AttributeError:
        pass
    form.fields['key'].widget.attrs['min'] = max_
    form.fields['key'].widget.attrs['value'] = max_


def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            progress = Progress(project_id=project.id)
            progress.save()
            editable = request.POST.copy()
            editable['project'] = project.id
            options_form = OptionsForm(editable)
            if options_form.is_valid():
                options_form.save()
            return redirect('index')
        else:
            raise Http404("Not valid")
    else:
        form = ProjectForm()
        options_form = OptionsForm()
    data = {'form': form, 'options_form': options_form}
    return render(request, 'add_project.html', data)
