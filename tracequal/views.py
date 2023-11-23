from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from api.models import Progress, Project
from utils.colors import calculate_gradient_color


def index(request):
    if request.user.is_authenticated:
        projects = Project.objects.filter(userproject__user=10)
        progress_ = Progress.objects.all().order_by('project_id')
        totals = []
        for prog in progress_:
            total = prog.progress_tests
            totals.append({
                'total': total,
                'color': calculate_gradient_color(total)
            })
        projects = zip(projects, totals)
        return render(request, 'index.html', {'projects': projects})
    else:
        return redirect("login")
        # return render(request, 'index.html')


def not_allowed(request):
    return render(request, 'notallowed.html')
