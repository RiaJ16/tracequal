from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('project/', views.project, name='project'),
    path('project/<int:project_id>', views.project, name='project'),
    path('user_stories/', views.user_stories, name='user_stories'),
    path('requirements/', views.requirements, name='requirements'),
    path('design/', views.design, name='design'),
    path('code/', views.code, name='code'),
    path('tests/', views.tests, name='tests'),
    path('user_stories/add/', views.add_user_story, name='add_user_story'),
    path('user_stories/edit/<int:us_id>', views.edit_user_story, name='edit_user_story'),
    path('user_stories/archive/', views.archive_user_story, name='archive_user_story'),
]
