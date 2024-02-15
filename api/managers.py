from django.db import models
from utils import update_progress

class LinkManager(models.Manager):
    def create(self, **kwargs):
        to_return = super().create(**kwargs)
        update_progress.update(kwargs.get('from_art').project_id)
        return to_return
