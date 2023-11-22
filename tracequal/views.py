from django.shortcuts import render
from django.urls import reverse_lazy

from api.models import Progress, Project
from utils.colors import calculate_gradient_color


def index(request):
    projects = Project.objects.all().order_by('id')
    progress_ = Progress.objects.all().order_by('project_id')
    totals = []
    for prog in progress_:
        total = (prog.progress_requirements +
                 prog.progress_design +
                 prog.progress_code +
                 prog.progress_tests) / 4
        total = prog.progress_tests
        totals.append({
            'total': total,
            'color': calculate_gradient_color(total)
        })
    projects = zip(projects, totals)
    return render(request, 'index.html', {'projects': projects})


def not_allowed(request):
    return render(request, 'notallowed.html')
