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
    path('add_user_story', views.add_user_story, name='add_user_story'),
]
