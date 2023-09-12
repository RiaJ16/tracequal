from django.contrib import admin

from .models import Artifact, Code, Design, Requirement, Test, UserStory

# Register your models here.

admin.site.register(UserStory)
admin.site.register(Code)
admin.site.register(Design)
admin.site.register(Requirement)
admin.site.register(Test)
