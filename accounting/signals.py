from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps
from accounting.models import User
from helpers import helpers


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, **kwargs):
    if instance.role:
        profile_model_class = apps.get_model('accounting', helpers.RELATED_PROFILE.get(instance.role))
        profile_model_class.objects.get_or_create(user=instance)
