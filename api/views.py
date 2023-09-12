from django.shortcuts import render

from .models import (Code, Design, Progress, Project, Requirement,
                     Test, UserStory)
from utils.colors import calculate_gradient_color
from utils.natural_language import determine_article

# Create your views here.


def project(request, project_id):
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


def user_stories(request, project_id):
    project_ = Project.objects.get(id=project_id)
    user_stories_ = UserStory.objects.filter(project_id=project_id)
    articles = []
    for user_story in user_stories_:
        articles.append(determine_article(user_story.usr))
    data = {
        'user_stories': user_stories_,
        'project': project_,
    }
    return render(request, 'user_stories.html', data)


def requirements(request, project_id):
    project_ = Project.objects.get(id=project_id)
    requirements_ = Requirement.objects.filter(project_id=project_id)
    data = {
        'requirements': requirements_,
        'project': project_,
    }
    return render(request, 'requirements.html', data)


def design(request, project_id):
    project_ = Project.objects.get(id=project_id)
    design_artifacts = Design.objects.filter(project_id=project_id)
    data = {
        'design_artifacts': design_artifacts,
        'project': project_,
    }
    return render(request, 'design.html', data)


def code(request, project_id):
    project_ = Project.objects.get(id=project_id)
    code_artifacts = Code.objects.filter(project_id=project_id)
    data = {
        'code_artifacts': code_artifacts,
        'project': project_,
    }
    return render(request, 'code.html', data)


def tests(request, project_id):
    project_ = Project.objects.get(id=project_id)
    tests_ = Test.objects.filter(project_id=project_id)
    classes = {
        'pass': ['btn-success', 'btn_pass'],
        'inconclusive': ['btn-secondary'],
        'fail': ['btn-danger'],
        'not tested': ['btn_not_tested'],
    }
    data = {
        'tests': tests_,
        'project': project_,
        'classes': classes,
    }
    return render(request, 'tests.html', data)
