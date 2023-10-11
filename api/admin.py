from django.contrib import admin

from .models import (Code, Design, Project, Requirement, Test, TestApplication,
                     UserStory)

# Register your models here.

admin.site.register(UserStory)
admin.site.register(Code)
admin.site.register(Design)
admin.site.register(Project)
admin.site.register(Requirement)
admin.site.register(Test)
admin.site.register(TestApplication)
