from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Patron


@receiver(post_save, sender=get_user_model())
def create_patron(sender, instance, created, **kwargs):
    if created:
        Patron.objects.create(user=instance)
