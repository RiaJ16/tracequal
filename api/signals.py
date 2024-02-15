from django.db.models.signals import post_save
from django.dispatch import receiver

from utils import update_progress

from .models import Artifact, Code, Design, Requirement, Test, UserStory


@receiver(post_save, sender=UserStory)
def after_save(sender, instance, created, **kwargs):
    update_progress.update(instance.project_id)

@receiver(post_save, sender=Requirement)
def after_save(sender, instance, created, **kwargs):
    update_progress.update(instance.project_id)

@receiver(post_save, sender=Design)
def after_save(sender, instance, created, **kwargs):
    update_progress.update(instance.project_id)

@receiver(post_save, sender=Code)
def after_save(sender, instance, created, **kwargs):
    update_progress.update(instance.project_id)

@receiver(post_save, sender=Test)
def after_save(sender, instance, created, **kwargs):
    update_progress.update(instance.project_id)

@receiver(post_save, sender=Artifact)
def after_save(sender, instance, created, **kwargs):
    print("archived ", sender)
    update_progress.update(instance.project_id)
