import copy
import json

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render

from .common import dict_with_sequences
from .forms import (CodeForm, DesignForm, OptionsForm, ProjectForm,
                    RequirementForm, TestForm, UserStoryForm)
from .models import (Code, Design, Options, Project, Requirement, Test,
                     UserProject, UserStory, Change)


def edit_user_story(request, project_id, us_id):
    if request.method == 'POST':
        us = UserStory.objects.get(id=us_id)
        us_copy = copy.deepcopy(us)
        form = UserStoryForm(request.POST, instance=us)
        if form.is_valid():
            form.save()
            save_change(us_copy, us, request.user)
            return redirect('user_stories')
        else:
            raise Http404("Not valid")
    else:
        us = UserStory.objects.get(id=us_id, project_id=project_id)
        form = UserStoryForm(instance=us)
    data = {'form': form, 'user_story': us}
    return render(request, 'edit_user_story.html', data)


def save_change(old_artifact, new_artifact, user):
    changes_dict = {}
    for key, value in new_artifact.__dict__.items():
        if key.startswith("_"):
            continue
        if not value == old_artifact.__dict__[key]:
            changes_dict[f'{key}_old'] = old_artifact.__dict__[key]
            changes_dict[f'{key}_new'] = value
    if changes_dict:
        change = Change(
            artifact_id=new_artifact.id,
            user=user,
            changes=json.dumps(changes_dict)
        )
        change.save()

def edit_requirement(request, project_id, id):
    if request.method == 'POST':
        requirement = Requirement.objects.get(id=id, project_id=project_id)
        rq_copy = copy.deepcopy(requirement)
        form = RequirementForm(
            dict_with_sequences(request.POST), instance=requirement)
        if form.is_valid():
            form.save()
            save_change(rq_copy, requirement, request.user)
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
        dn_copy = copy.deepcopy(design)
        form = DesignForm(request.POST, request.FILES, instance=design)
        if form.is_valid():
            form.save()
            save_change(dn_copy, design, request.user)
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
        cd_copy = copy.deepcopy(code)
        form = CodeForm(request.POST, instance=code)
        if form.is_valid():
            form.save()
            save_change(cd_copy, code, request.user)
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
        ts_copy = copy.deepcopy(test)
        form = TestForm(request.POST, instance=test)
        if form.is_valid():
            form.save()
            save_change(ts_copy, test, request.user)
            return redirect('tests')
        else:
            raise Http404("Not valid")
    else:
        test = Test.objects.get(id=test_id, project_id=project_id)
        form = TestForm(instance=test)
    data = {'form': form, 'test': test}
    return render(request, 'edit_test.html', data)


@login_required
def edit_project(request, project_id):
    project = Project.objects.get(id=project_id)
    try:
        role = UserProject.objects.get(
            user_id=request.user.id, project_id=project.id).role
        if not role == "admin" and not role == "superadmin":
            raise UserProject.DoesNotExist
    except UserProject.DoesNotExist:
        return redirect('index')
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
