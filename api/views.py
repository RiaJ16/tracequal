from django.shortcuts import redirect, render
from functools import wraps

from .models import (Code, Design, Options, Progress, Project, Requirement,
                     Test, UserStory)
from utils.colors import calculate_gradient_color
from utils.natural_language import determine_article

from . import add, edit

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


def project(request, project_id=None):
    if project_id:
        try:
            Project.objects.get(id=project_id)
            request.session['selected_project'] = project_id
        except Project.DoesNotExist:
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
        project_id=project_id).order_by('id')
    try:
        options = Options.objects.get(project_id=project_id)
        prefix = options.prefix_us
    except Options.DoesNotExist:
        prefix = ''
    data = {
        'user_stories': user_stories_,
        'prefix': prefix,
    }
    return render(request, 'user_stories.html', data)


@project_required
def requirements(request, project_id):
    requirements_ = Requirement.objects.filter(
        project_id=project_id).order_by('id')
    try:
        options = Options.objects.get(project_id=project_id)
        prefix = options.prefix_req
    except Options.DoesNotExist:
        prefix = ''
    data = {
        'requirements': requirements_,
        'prefix': prefix,
    }
    return render(request, 'requirements.html', data)


@project_required
def design(request, project_id):
    design_artifacts = Design.objects.filter(
        project_id=project_id).order_by('id')
    try:
        options = Options.objects.get(project_id=project_id)
        prefix = options.prefix_design
    except Options.DoesNotExist:
        prefix = ''
    data = {
        'design_artifacts': design_artifacts,
        'prefix': prefix,
    }
    return render(request, 'design.html', data)


@project_required
def code(request, project_id):
    code_artifacts = Code.objects.filter(
        project_id=project_id).order_by('id')
    try:
        options = Options.objects.get(project_id=project_id)
        prefix = options.prefix_code
    except Options.DoesNotExist:
        prefix = ''
    data = {
        'code_artifacts': code_artifacts,
        'prefix': prefix,
    }
    return render(request, 'code.html', data)


@project_required
def tests(request, project_id):
    tests_ = Test.objects.filter(project_id=project_id).order_by('id')
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
    }
    return render(request, 'tests.html', data)


@project_required
def add_user_story(request, project_id):
    return add.add_user_story(request, project_id)


@project_required
def edit_user_story(request, project_id, us_id):
    return edit.edit_user_story(request, project_id, us_id)
