from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('project/<int:project_id>', views.project, name='project'),
    path('user_stories/<int:project_id>', views.user_stories, name='user_stories'),
    path('requirements/<int:project_id>', views.requirements, name='requirements'),
    path('design/<int:project_id>', views.design, name='design'),
    path('code/<int:project_id>', views.code, name='code'),
    path('tests/<int:project_id>', views.tests, name='tests'),
]
