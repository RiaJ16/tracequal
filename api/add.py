import json

from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render

from .common import dict_with_sequences
from .forms import *
from .models import (Artifact, Code, Design, Progress, Project, Requirement,
                     Test, UserStory)


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
        form.fields['type'].initial = "user_story"
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
        form.fields['type'].initial = "requirement"
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
        form.fields['type'].initial = "design"
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
        form.fields['type'].initial = "code"
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
        form.fields['type'].initial = "test"
    set_current_key(form, Test, project_id)
    return render(request, 'add_test.html', {'form': form})


def add_test_application(request, project_id, test_id):
    if request.method == 'POST':
        form = TestApplicationForm(request.POST)
        if form.is_valid():
            ta = form.save()
            test = ta.test
            tapps = TestApplication.objects.filter(test=test)
            if tapps:
                tapps = sorted(
                    tapps, key=lambda x: x.application_date, reverse=True)
                ta = tapps[0]
            test.verdict = ta.verdict
            test.application_date = ta.application_date
            test.save()
            return redirect('tests')
        else:
            raise Http404('Not valid')
    else:
        form = TestApplicationForm()
        form.fields['test'].initial = Test.objects.get(
            id=test_id, project_id=project_id,)
    return render(request, 'add_test_application.html', {'form': form})


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


def add_link(request, project_id, artifact_id):
    artifact = Artifact.objects.get(project_id=project_id, id=artifact_id)
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        types = ['evolution', 'dependency']
        if data:
            for link_data in data:
                target = Artifact.objects.get(
                    project_id=project_id, id=link_data['artifact'])
                link = Link(from_art=artifact, to_art=target,
                            type=types[link_data['type']])
                link.save()
            return JsonResponse({'message': 'Success'})
        else:
            raise Http404('Not valid')
    else:
        form = LinkForm()
        form.fields['from_art'].initial = artifact
        artifacts = Artifact.objects.filter(project_id=project_id)
        links = Link.objects.filter(from_art=artifact)
        artifacts_to_exclude = [artifact.id]
        artifacts = [artifact for artifact in artifacts if
                     artifact.id not in artifacts_to_exclude]
        for link in links:
            if link.type == 'evolution':
                artifact_ = next((
                    artifact_ for artifact_ in artifacts
                    if artifact_ == link.to_art), None)
                if artifact_:
                    artifact_.evolution = True
            if link.type == 'dependency':
                artifact_ = next((
                    artifact_ for artifact_ in artifacts
                    if artifact_ == link.to_art), None)
                if artifact_:
                    artifact_.dependency = True
        context = {
            'form': form,
            'artifact': artifact,
            'artifacts': artifacts,
        }
        return render(request, 'add_link.html', context)
