import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from functools import wraps

from .models import (Artifact, Code, Design, Link, Options, Progress, Project,
                     Requirement, Test, TestApplication, UserProject, UserStory)
from utils.colors import calculate_gradient_color

from . import add, archive, edit
from .archive import admin_required

# Create your views here.


def project_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            project_id = request.session['selected_project']
        except KeyError:
            return redirect('index')  # Redirect if project is not selected
        return view_func(request, project_id, *args, **kwargs)
    return wrapper


@login_required
def project(request, project_id=None):
    if project_id:
        try:
            Project.objects.get(id=project_id)
            role = UserProject.objects.get(
                project_id=project_id, user_id=request.user.id).role
            request.session['selected_project'] = project_id
            request.session['role'] = role
        except (Project.DoesNotExist, UserProject.DoesNotExist):
            pass
        return redirect('project')
    else:
        try:
            project_id = request.session['selected_project']
        except KeyError:
            return redirect('index')
    project_ = Project.objects.get(id=project_id)
    progress_ = Progress.objects.get(project_id=project_id)
    total = (progress_.progress_requirements +
             progress_.progress_design +
             progress_.progress_code +
             progress_.progress_tests) / 4
    colors = {
        'r': calculate_gradient_color(progress_.progress_requirements),
        'd': calculate_gradient_color(progress_.progress_design),
        'c': calculate_gradient_color(progress_.progress_code),
        't': calculate_gradient_color(progress_.progress_tests),
        'total': calculate_gradient_color(total)
    }
    data = {
        'project': project_,
        'progress': progress_,
        'colors': colors,
        'total': total,
    }
    return render(request, 'project.html', data)


@project_required
def user_stories(request, project_id):
    user_stories_ = UserStory.objects.filter(
        project_id=project_id, archived=False).order_by('id')
    try:
        options = Options.objects.get(project_id=project_id)
        prefix = options.prefix_us
    except Options.DoesNotExist:
        prefix = ''
    data = {
        'user_stories': user_stories_,
        'prefix': prefix,
        'role': request.session['role'],
    }
    return render(request, 'user_stories.html', data)


@project_required
def requirements(request, project_id):
    requirements_ = Requirement.objects.filter(
        project_id=project_id, archived=False).order_by('id')
    try:
        options = Options.objects.get(project_id=project_id)
        prefix = options.prefix_req
    except Options.DoesNotExist:
        prefix = ''
    data = {
        'requirements': requirements_,
        'prefix': prefix,
        'role': request.session['role'],
    }
    return render(request, 'requirements.html', data)


@project_required
def design(request, project_id):
    design_artifacts = Design.objects.filter(
        project_id=project_id, archived=False).order_by('id')
    try:
        options = Options.objects.get(project_id=project_id)
        prefix = options.prefix_design
    except Options.DoesNotExist:
        prefix = ''
    data = {
        'design_artifacts': design_artifacts,
        'prefix': prefix,
        'role': request.session['role'],
    }
    return render(request, 'design.html', data)


@project_required
def code(request, project_id):
    code_artifacts = Code.objects.filter(
        project_id=project_id, archived=False).order_by('id')
    try:
        options = Options.objects.get(project_id=project_id)
        prefix = options.prefix_code
    except Options.DoesNotExist:
        prefix = ''
    data = {
        'code_artifacts': code_artifacts,
        'prefix': prefix,
        'role': request.session['role'],
    }
    return render(request, 'code.html', data)


@project_required
def tests(request, project_id):
    tests_ = Test.objects.filter(
        project_id=project_id, archived=False).order_by('id')
    try:
        options = Options.objects.get(project_id=project_id)
        prefix = options.prefix_test
    except Options.DoesNotExist:
        prefix = ''
    classes = {
        'pass': ['btn-success', 'btn_pass'],
        'inconclusive': ['btn_inconclusive'],
        'fail': ['btn-danger'],
        'not tested': ['btn-secondary'],
    }
    data = {
        'tests': tests_,
        'classes': classes,
        'prefix': prefix,
        'role': request.session['role'],
    }
    return render(request, 'tests.html', data)


@project_required
def add_user_story(request, project_id):
    return add.add_user_story(request, project_id)


@project_required
def edit_user_story(request, project_id, us_id):
    return edit.edit_user_story(request, project_id, us_id)


@project_required
def archive_user_story(request, project_id):
    return archive.archive_user_story(request, project_id)


@project_required
def add_requirement(request, project_id):
    return add.add_requirement(request, project_id)


@project_required
def edit_requirement(request, project_id, id):
    return edit.edit_requirement(request, project_id, id)


@project_required
def archive_requirement(request, project_id):
    return archive.archive_requirement(request, project_id)


@project_required
def add_design(request, project_id):
    return add.add_design(request, project_id)


@project_required
def edit_design(request, project_id, id):
    return edit.edit_design(request, project_id, id)


@project_required
def archive_design(request, project_id):
    return archive.archive_design(request, project_id)


@project_required
def add_code(request, project_id):
    return add.add_code(request, project_id)


@project_required
def edit_code(request, project_id, id):
    return edit.edit_code(request, project_id, id)


@project_required
def archive_code(request, project_id):
    return archive.archive_code(request, project_id)


@project_required
def add_test(request, project_id):
    return add.add_test(request, project_id)


@project_required
def edit_test(request, project_id, id):
    return edit.edit_test(request, project_id, id)


@project_required
def archive_test(request, project_id):
    return archive.archive_test(request, project_id)


@project_required
def archive_test(request, project_id):
    return archive.archive_test(request, project_id)


def add_project(request):
    return add.add_project(request)


def edit_project(request, id):
    return edit.edit_project(request, id)


@project_required
def add_test_application(request, project_id, test_id=None):
    return add.add_test_application(request, project_id, test_id)


@project_required
def delete_test_application(request, project_id):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body.decode('utf-8'))
            ta_id = json_data.get('ta_id')
            ta = TestApplication.objects.get(id=ta_id)
            test = ta.test
            ta.delete()
            tapps = TestApplication.objects.filter(test=test)
            if tapps:
                tapps = sorted(
                    tapps, key=lambda x: x.application_date, reverse=True)
                tapp = tapps[0]
                test.verdict = tapp.verdict
                test.application_date = tapp.application_date
            else:
                test.verdict = "not tested"
                test.application_date = None
            test.save()
        except TestApplication.DoesNotExist:
            raise Http404("Not valid")
    return redirect('tests')


@project_required
def retrieve_test(request, project_id, id):
    if request.method == 'POST':
        try:
            test = Test.objects.get(id=id, project_id=project_id)
            json_data = {
                'id': test.id,
                'verdict': test.verdict,
                'verdict_cap': test.verdict.capitalize(),
                'application_date': test.application_date,
                'test_applications': len(test.test_applications.all()),
            }
            return JsonResponse(json_data)
        except Test.DoesNotExist:
            raise Http404("Not valid")
    else:
        return redirect('tests')


@project_required
def links(request, project_id, artifact_id):
    return show_links(request, project_id, artifact_id)


def show_links(request, project_id, artifact_id, archive_=False):
    try:
        artifact = Artifact.objects.get(id=artifact_id, project=project_id)
        from_links = Link.objects.filter(
            from_art=artifact_id,
            archived=archive_).order_by('id')
        to_links = Link.objects.filter(
            to_art=artifact_id,
            archived=archive_).order_by('id')
        all_links_ = Link.objects.filter(
            Q(archived=archive_) & (Q(from_art=artifact_id) | Q(to_art=artifact_id))
        )
        views_dict = {
            'user_story': 'user_stories',
            'requirement': 'requirements',
            'design': 'design',
            'code': 'code',
            'test': 'tests',
        }
        graph_data_json = get_graph_data_json(project_id, all_links_, artifact)
        data = {
            'from_links': from_links,
            'to_links': to_links,
            'artifact': artifact,
            'graph_data_json': graph_data_json,
            'view_name': views_dict[artifact.type],
            "archive": archive_,
            'role': request.session['role'],
        }
        return render(request, 'links.html', data)
    except Artifact.DoesNotExist:
        return redirect('index')


@project_required
def add_link(request, project_id, artifact_id):
    return add.add_link(request, project_id, artifact_id)


@project_required
def traceability(request, project_id):
    links_ = Link.objects.filter(from_art__project=project_id)
    graph_data_json = get_graph_data_json(project_id, links_)
    context = {
        'links': links_,
        'graph_data_json': graph_data_json,
    }
    return render(request, 'traceability.html', context)


def get_graph_data_json(project_id, all_links_, artifact=None):
    options = Options.objects.get(project_id=project_id)
    options_dict = {
        'user_story': options.prefix_us,
        'requirement': options.prefix_req,
        'design': options.prefix_design,
        'code': options.prefix_code,
        'test': options.prefix_test,
    }
    links_ = []
    for link in all_links_:
        arrowhead = '' if link.type == 'evolution' else '2'
        links_.append({
            "id": link.id,
            "source": link.from_art.id,
            "target": link.to_art.id,
            "type": link.type,
            "arrowhead": arrowhead,
        })
    linked_artifacts = {}
    for link in all_links_:
        linked_artifacts[link.from_art] = True
        linked_artifacts[link.to_art] = True
    unique_artifacts = list(linked_artifacts.keys())
    nodes_ = []
    for artifact_ in unique_artifacts:
        main = ""
        if artifact:
            main = "main" if artifact == artifact_ else ""
        type_ = artifact_.type.replace('_', ' ').capitalize()
        nodes_.append({
            "id": artifact_.id,
            "name": f"{type_} {artifact_.key} - {artifact_.name}",
            "type": f"{artifact_.type}",
            "key": f"{options_dict[artifact_.type]}{artifact_.key}",
            "main": main,
        })
    graph_data = {"nodes": nodes_, "links": links_}
    return json.dumps(graph_data)


@project_required
def archive_link(request, project_id):
    return archive.archive_link(request, project_id)


@project_required
@admin_required
def links_archive(request, role, project_id, artifact_id):
    if not role == "admin":
        return redirect('index')
    if request.method == 'POST':
        raise Http404("Not valid")
    else:
        return show_links(request, project_id, artifact_id, True)
