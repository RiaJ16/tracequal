from django.contrib import admin

from .models import (Code, Design, Link, Project, Requirement, Test,
                     TestApplication, UserStory, Usr)

# Register your models here.

admin.site.register(UserStory)
admin.site.register(Code)
admin.site.register(Design)
admin.site.register(Link)
admin.site.register(Project)
admin.site.register(Requirement)
admin.site.register(Test)
admin.site.register(TestApplication)
admin.site.register(Usr)
