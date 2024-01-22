import json

from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from functools import wraps

from .models import (Artifact, Code, Design, Link, Options, Requirement, Test,
                     UserStory)


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            role = request.session['role']
        except KeyError:
            return redirect('index')  # Redirect if project is not selected
        return view_func(request, role, *args, **kwargs)
    return wrapper


@admin_required
def archive_user_story(request, role, project_id):
    if request.method == 'POST':
        return archive_artifact(request, role)
    else:
        artifacts = UserStory.objects.filter(
            project_id=project_id, archived=True).order_by('id')
        try:
            options = Options.objects.get(project_id=project_id)
            prefix = options.prefix_us
        except Options.DoesNotExist:
            prefix = ''
        artifacts_data = {
            'key': 'user_stories',
            'template': 'user_stories.html',
            'artifacts': artifacts,
            'prefix': prefix,
        }
        return archive_artifact(request, role, artifacts_data)


@admin_required
def archive_requirement(request, role, project_id):
    if request.method == 'POST':
        return archive_artifact(request, role)
    else:
        artifacts = Requirement.objects.filter(
            project_id=project_id, archived=True).order_by('id')
        try:
            options = Options.objects.get(project_id=project_id)
            prefix = options.prefix_req
        except Options.DoesNotExist:
            prefix = ''
        artifacts_data = {
            'key': 'requirements',
            'template': 'requirements.html',
            'artifacts': artifacts,
            'prefix': prefix,
        }
        return archive_artifact(request, role, artifacts_data)


@admin_required
def archive_design(request, role, project_id):
    if request.method == 'POST':
        return archive_artifact(request, role)
    else:
        artifacts = Design.objects.filter(
            project_id=project_id, archived=True).order_by('id')
        try:
            options = Options.objects.get(project_id=project_id)
            prefix = options.prefix_design
        except Options.DoesNotExist:
            prefix = ''
        artifacts_data = {
            'key': 'design_artifacts',
            'template': 'design.html',
            'artifacts': artifacts,
            'prefix': prefix,
        }
        return archive_artifact(request, role, artifacts_data)


@admin_required
def archive_code(request, role, project_id):
    if request.method == 'POST':
        return archive_artifact(request, role)
    else:
        artifacts = Code.objects.filter(
            project_id=project_id, archived=True).order_by('id')
        try:
            options = Options.objects.get(project_id=project_id)
            prefix = options.prefix_code
        except Options.DoesNotExist:
            prefix = ''
        artifacts_data = {
            'key': 'code_artifacts',
            'template': 'code.html',
            'artifacts': artifacts,
            'prefix': prefix,
        }
        return archive_artifact(request, role, artifacts_data)


@admin_required
def archive_test(request, role, project_id):
    if request.method == 'POST':
        return archive_artifact(request, role)
    else:
        artifacts = Test.objects.filter(
            project_id=project_id, archived=True).order_by('id')
        try:
            options = Options.objects.get(project_id=project_id)
            prefix = options.prefix_test
        except Options.DoesNotExist:
            prefix = ''
        artifacts_data = {
            'key': 'tests',
            'template': 'tests.html',
            'artifacts': artifacts,
            'prefix': prefix,
        }
        return archive_artifact(request, role, artifacts_data)


def archive_artifact(request, role, artifacts_data=None):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        artifact = Artifact.objects.get(id=data.get('id'))
        artifact.archived = data.get('archive')
        artifact.save()
        return JsonResponse({'message': 'Success'})
    else:
        if not role == "admin" and not role == "superadmin":
            return redirect('index')
        data = {
            artifacts_data['key']: artifacts_data['artifacts'],
            'prefix': artifacts_data['prefix'],
            'archive': True,
        }
        return render(request, artifacts_data['template'], data)


def archive_link(request, project_id):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        link = Link.objects.get(id=data.get('id'), from_art__project=project_id)
        link.archived = data.get('archive')
        link.save()
        return JsonResponse({'message': 'Success'})
    else:
        raise Http404("Not valid")
