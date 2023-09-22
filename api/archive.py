import json

from django.http import JsonResponse
from django.shortcuts import redirect, render

from .models import Artifact, Options, UserStory


def archive_user_story(request, project_id):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        us = Artifact.objects.get(id=data.get('id'))
        us.archived = data.get('archive')
        us.save()
        return JsonResponse({'message': 'Success'})
    else:
        user_stories_ = UserStory.objects.filter(
            project_id=project_id, archived=True).order_by('id')
        try:
            options = Options.objects.get(project_id=project_id)
            prefix = options.prefix_us
        except Options.DoesNotExist:
            prefix = ''
        data = {
            'user_stories': user_stories_,
            'prefix': prefix,
            'archive': True,
        }
        return render(request, 'user_stories.html', data)
