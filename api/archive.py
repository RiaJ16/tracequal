import json

from django.http import JsonResponse
from django.shortcuts import redirect, render

from .models import Artifact, Code, Design, Options, Requirement, UserStory


def archive_user_story(request, project_id):
    if request.method == 'POST':
        return archive_artifact(request, project_id)
    else:
        artifacts = UserStory.objects.filter(
            project_id=project_id, archived=True).order_by('id')
        artifacts_data = {
            'key': 'user_stories',
            'template': 'user_stories.html',
            'artifacts': artifacts
        }
        return archive_artifact(request, project_id, artifacts_data)


def archive_requirement(request, project_id):
    if request.method == 'POST':
        return archive_artifact(request, project_id)
    else:
        artifacts = Requirement.objects.filter(
            project_id=project_id, archived=True).order_by('id')
        artifacts_data = {
            'key': 'requirements',
            'template': 'requirements.html',
            'artifacts': artifacts
        }
        return archive_artifact(request, project_id, artifacts_data)


def archive_design(request, project_id):
    if request.method == 'POST':
        return archive_artifact(request, project_id)
    else:
        artifacts = Design.objects.filter(
            project_id=project_id, archived=True).order_by('id')
        artifacts_data = {
            'key': 'design_artifacts',
            'template': 'design.html',
            'artifacts': artifacts
        }
        return archive_artifact(request, project_id, artifacts_data)


def archive_code(request, project_id):
    if request.method == 'POST':
        return archive_artifact(request, project_id)
    else:
        artifacts = Code.objects.filter(
            project_id=project_id, archived=True).order_by('id')
        artifacts_data = {
            'key': 'code_artifacts',
            'template': 'code.html',
            'artifacts': artifacts
        }
        return archive_artifact(request, project_id, artifacts_data)


def archive_artifact(request, project_id, artifacts_data=None):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        artifact = Artifact.objects.get(id=data.get('id'))
        artifact.archived = data.get('archive')
        artifact.save()
        return JsonResponse({'message': 'Success'})
    else:
        try:
            options = Options.objects.get(project_id=project_id)
            prefix = options.prefix_us
        except Options.DoesNotExist:
            prefix = ''
        data = {
            artifacts_data['key']: artifacts_data['artifacts'],
            'prefix': prefix,
            'archive': True,
        }
        return render(request, artifacts_data['template'], data)
