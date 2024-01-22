from django.urls import reverse
from api.sitemap import resolve

from api.models import Artifact, Options, Project


def generate_breadcrumbs(request):
    path = request.path
    path_items = path.split('/')[1:]
    if len(path_items) > 1 and path_items[-1] == '':
        path_items.pop()
    try:
        options = Options.objects.get(project_id=request.session['selected_project'])
        types_dict = {
            'user_story': ('user_stories', options.prefix_us),
            'requirement': ('requirements', options.prefix_req),
            'design': ('design', options.prefix_design),
            'code': ('code', options.prefix_code),
            'test': ('tests', options.prefix_test),
        }
    except KeyError:
        types_dict = {}
    if path_items[0] == 'project' or path_items[0] == 'manage_users':
        try:
            if path_items[1] == 'add':
                breadcrumbs = resolve('add_project')
                return breadcrumbs
            project = Project.objects.get(id=path_items[-1])
            if path_items[1] == 'edit':
                breadcrumbs = resolve('edit_project')
                breadcrumb_id = next((id_ for id_ in range(len(breadcrumbs)) if
                                      breadcrumbs[id_].get(
                                          'url') == 'edit_project'), None)
            else:
                breadcrumbs = resolve('manage_users')
                breadcrumb_id = next((id_ for id_ in range(len(breadcrumbs)) if
                                      breadcrumbs[id_].get(
                                          'url') == 'manage_users'), None)
            if breadcrumb_id:
                breadcrumb = breadcrumbs[breadcrumb_id]
                breadcrumb['label'] = f"{breadcrumb['label']} ({project.name})"
            return breadcrumbs
        except IndexError:
            pass
    if path_items[0] == 'links' or path_items[0] == 'add_link':
        artifact_id = path_items[1]
        artifact = Artifact.objects.get(id=artifact_id)
        breadcrumbs = resolve(types_dict[artifact.type][0])
        breadcrumbs.append({
            'url': 'links',
            'label': f'Links ({types_dict[artifact.type][1]}{artifact.key})',
            'artifact_id': artifact_id,
        })
        if path_items[0] == 'add_link':
            breadcrumbs.append({
                'url': '',
                'label': f'Add links from {types_dict[artifact.type][1]}{artifact.key}'
            })
    else:
        breadcrumbs = resolve(path_items[0])
    breadcrumb = next((breadcrumb for breadcrumb in breadcrumbs if
                       breadcrumb.get('url') == 'project'), None)
    if breadcrumb:
        project = Project.objects.get(id=request.session['selected_project'])
        breadcrumb['label'] = truncate_string(project.name, 16)
    special_pages = {
        'archive': 'Archive',
        'add': 'Add',
        'edit': 'Edit',
    }
    try:
        for key, item in special_pages.items():
            artifact_id = None
            for path_item in path_items:
                try:
                    artifact_id = int(path_item)
                except ValueError:
                    pass
            if artifact_id:
                artifact = Artifact.objects.get(id=artifact_id)
                label = f"{item} ({types_dict.get(artifact.type)[1]}{artifact.key})"
            else:
                label = item
            if key in path_items:
                breadcrumbs.append({
                    'url': '',
                    'label': label,
                })
    except IndexError:
        pass
    return breadcrumbs


def truncate_string(input_string, max_length):
    if len(input_string) <= max_length:
        return input_string
    else:
        return input_string[:max_length - 3] + "..."
