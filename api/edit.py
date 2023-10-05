from django.http import Http404
from django.shortcuts import redirect, render

from .common import dict_with_sequences
from .forms import (CodeForm, DesignForm, OptionsForm, ProjectForm,
                    RequirementForm, TestForm, UserStoryForm)
from .models import Code, Design, Options, Project, Requirement, Test, UserStory


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


def edit_code(request, project_id, code_id):
    if request.method == 'POST':
        code = Code.objects.get(id=code_id)
        form = CodeForm(request.POST, instance=code)
        if form.is_valid():
            form.save()
            return redirect('code')
        else:
            raise Http404("Not valid")
    else:
        code = Code.objects.get(id=code_id, project_id=project_id)
        form = CodeForm(instance=code)
    data = {'form': form, 'code': code}
    return render(request, 'edit_code.html', data)


def edit_test(request, project_id, test_id):
    if request.method == 'POST':
        test = Test.objects.get(id=test_id)
        form = TestForm(request.POST, instance=test)
        if form.is_valid():
            form.save()
            return redirect('tests')
        else:
            raise Http404("Not valid")
    else:
        test = Test.objects.get(id=test_id, project_id=project_id)
        form = TestForm(instance=test)
    data = {'form': form, 'test': test}
    return render(request, 'edit_test.html', data)


def edit_project(request, project_id):
    project = Project.objects.get(id=project_id)
    options = Options.objects.get(project_id=project.id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            options_form = OptionsForm(request.POST, instance=options)
            if options_form.is_valid():
                options_form.save()
            return redirect('index')
        else:
            raise Http404("Not valid")
    else:
        form = ProjectForm(instance=project)
        options_form = OptionsForm(instance=options)
    data = {'form': form, 'options_form': options_form}
    return render(request, 'add_project.html', data)
