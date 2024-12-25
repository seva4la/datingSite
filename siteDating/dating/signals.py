import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import User


@receiver(post_delete, sender=User)
def delete_profile_image(sender, instance, **kwargs):

    if instance.profile_image:
        image_path = instance.profile_image.path
        if os.path.isfile(image_path):
            os.remove(image_path)