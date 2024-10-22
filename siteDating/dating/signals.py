import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import User


@receiver(post_delete, sender=User)
def delete_profile_image(sender, instance, **kwargs):
    """
    Удаляет изображение профиля с файловой системы при удалении пользователя.
    """
    if instance.profile_image:
        # Получаем путь к изображению
        image_path = instance.profile_image.path

        # Проверяем, существует ли файл, и удаляем его
        if os.path.isfile(image_path):
            os.remove(image_path)