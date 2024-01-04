from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from api.models import Progress, Project, UserProject
from utils.colors import calculate_gradient_color


def index(request):
    if request.user.is_authenticated:
        projects = Project.objects.filter(userproject__user=request.user.id)
        progress_ = Progress.objects.filter(project__userproject__user=request.user.id).order_by('project_id')
        permissions = []
        for project in projects:
            permission = UserProject.objects.get(
                user_id=request.user.id, project_id=project.id)
            permissions.append(permission.role)
        totals = []
        for prog in progress_:
            total = prog.progress_tests
            totals.append({
                'total': total,
                'color': calculate_gradient_color(total)
            })
        are_projects = bool(projects)
        projects = zip(projects, totals, permissions)
        context = {'projects': projects, 'are_projects': are_projects}
        return render(request, 'index.html', context)
    else:
        return redirect("login")
        # return render(request, 'index.html')


def not_allowed(request):
    return render(request, 'notallowed.html')
