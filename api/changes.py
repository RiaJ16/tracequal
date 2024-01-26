import difflib
import json

from django.urls import reverse
from django.shortcuts import render

from api.models import Artifact, Change


def show_changes(request, project_id, artifact_id):
    artifact = Artifact.objects.get(id=artifact_id, project_id=project_id)
    urls = {
        'user_story': reverse('user_stories'),
        'requirement': reverse('requirements'),
        'design': reverse('design'),
        'code': reverse('code'),
        'test': reverse('tests'),
    }
    changes = Change.objects.filter(artifact_id=artifact_id).order_by('-date')
    for change in changes:
        keys = []
        changes_json = []
        for key, value in change.changes.items():
            keys.append(key.rsplit('_', 1)[0])
        keys = set(keys)
        for key in keys:
            differences = highlight_worddiff(
                change.changes[f"{key}_old"],
                change.changes[f"{key}_new"]
            )
            changes_json.append({
                'attribute': key,
                'old': change.changes[f"{key}_old"],
                'new': change.changes[f"{key}_new"],
                'differences': differences,
            })
        change.changes_json = changes_json
    context = {
        'artifact': artifact,
        'changes': changes,
        'back_url': urls[artifact.type],
    }
    return render(request, 'changes.html', context)


def highlight_worddiff(string1, string2):
    if not string1:
        string1 = ''
    if not string2:
        string2 = ''
    if not type(string1) == str:
        string1 = json.dumps(string1)
    if not type(string2) == str:
        string2 = json.dumps(string2)
    words1 = string1.split()
    words2 = string2.split()

    d = difflib.Differ()
    diff = list(d.compare(words1, words2))

    highlighted_diff = []
    for word_diff in diff:
        if word_diff.startswith(' '):
            highlighted_diff.append(word_diff)
        elif word_diff.startswith('-'):
            highlighted_diff.append(
                f'<b class="old">{word_diff[2:]}</b>')
        elif word_diff.startswith('+'):
            highlighted_diff.append(
                f'<b class="new">{word_diff[2:]}</b>')
    return ' '.join(highlighted_diff)