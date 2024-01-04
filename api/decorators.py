from django.shortcuts import redirect
from functools import wraps

from .models import Project, UserProject


def privileged(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        project_id = kwargs.get('project_id')
        project_ = Project.objects.get(id=project_id)
        try:
            role = UserProject.objects.get(
                user_id=request.user.id, project_id=project_.id).role
            if not (role == "admin" or role == "superadmin"):
                raise UserProject.DoesNotExist
        except UserProject.DoesNotExist:
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return wrapped_view
