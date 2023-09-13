from django.shortcuts import redirect, render

from .models import (Code, Design, Progress, Project, Requirement,
                     Test, UserStory)
from utils.colors import calculate_gradient_color
from utils.natural_language import determine_article

from . import add

# Create your views here.


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


def user_stories(request):
    try:
        project_id = request.session['selected_project']
    except KeyError:
        return redirect('index')
    user_stories_ = UserStory.objects.filter(project_id=project_id)
    articles = []
    for user_story in user_stories_:
        articles.append(determine_article(user_story.usr))
    data = {
        'user_stories': user_stories_,
    }
    return render(request, 'user_stories.html', data)


def requirements(request):
    try:
        project_id = request.session['selected_project']
    except KeyError:
        return redirect('index')
    requirements_ = Requirement.objects.filter(project_id=project_id)
    data = {
        'requirements': requirements_,
    }
    return render(request, 'requirements.html', data)


def design(request):
    try:
        project_id = request.session['selected_project']
    except KeyError:
        return redirect('index')
    design_artifacts = Design.objects.filter(project_id=project_id)
    data = {
        'design_artifacts': design_artifacts,
    }
    return render(request, 'design.html', data)


def code(request):
    try:
        project_id = request.session['selected_project']
    except KeyError:
        return redirect('index')
    code_artifacts = Code.objects.filter(project_id=project_id)
    data = {
        'code_artifacts': code_artifacts,
    }
    return render(request, 'code.html', data)


def tests(request):
    try:
        project_id = request.session['selected_project']
    except KeyError:
        return redirect('index')
    tests_ = Test.objects.filter(project_id=project_id)
    classes = {
        'pass': ['btn-success', 'btn_pass'],
        'inconclusive': ['btn_inconclusive'],
        'fail': ['btn-danger'],
        'not tested': ['btn-secondary'],
    }
    data = {
        'tests': tests_,
        'classes': classes,
    }
    return render(request, 'tests.html', data)


def add_user_story(request):
    return add.add_user_story(request)
