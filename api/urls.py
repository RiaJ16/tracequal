from django.urls import include, path, re_path

from . import views




urlpatterns = [
    path('project/', views.project, name='project'),
    path('project/<int:project_id>', views.project, name='project'),
    path('project/add', views.add_project, name='add_project'),
    path('project/edit/<int:id>', views.edit_project, name='edit_project'),
    path('user_stories/', views.user_stories, name='user_stories'),
    path('requirements/', views.requirements, name='requirements'),
    path('design/', views.design, name='design'),
    path('code/', views.code, name='code'),
    path('tests/', views.tests, name='tests'),
    path('traceability/', views.traceability, name='traceability'),
    path('links/<int:artifact_id>/', views.links, name='links'),
    path('user_stories/add/', views.add_user_story, name='add_user_story'),
    path('user_stories/edit/<int:us_id>', views.edit_user_story,
         name='edit_user_story'),
    path('user_stories/archive/', views.archive_user_story,
         name='archive_user_story'),
    path('requirements/add/', views.add_requirement, name='add_requirement'),
    path('requirements/edit/<int:id>', views.edit_requirement,
         name='edit_requirement'),
    path('requirements/archive/', views.archive_requirement,
         name='archive_requirement'),
    path('design/add/', views.add_design, name='add_design'),
    path('design/edit/<int:id>/', views.edit_design, name='edit_design'),
    path('design/archive/', views.archive_design, name='archive_design'),
    path('code/add/', views.add_code, name='add_code'),
    path('code/edit/<int:id>/', views.edit_code, name='edit_code'),
    path('code/archive/', views.archive_code, name='archive_code'),
    path('tests/add/', views.add_test, name='add_test'),
    path('tests/edit/<int:id>/', views.edit_test, name='edit_test'),
    path('tests/archive/', views.archive_test, name='archive_test'),
    re_path(r'^tests_applications/add/(?P<test_id>[\w-]+)?/$',
            views.add_test_application, name='add_test_application'),
    path('test_applications/delete/', views.delete_test_application,
         name='delete_test_application'),
    path('test/<int:id>/', views.retrieve_test, name='retrieve_test'),
    path('add_link/<int:artifact_id>/', views.add_link, name='add_link'),
    path('links/archive/', views.archive_link, name='archive_link'),
]
