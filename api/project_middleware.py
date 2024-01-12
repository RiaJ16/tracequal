from .models import Project


class ProjectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        project_id = request.session.get('selected_project')

        project = None
        if project_id:
            project = Project.objects.get(id=project_id)

        request.project = project
        response = self.get_response(request)
        return response
