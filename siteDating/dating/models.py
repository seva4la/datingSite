from tkinter import Image

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import ForeignKey, PROTECT
import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission


def validate_age(value):
    if value < 18 or value > 99:
        raise ValidationError('Возраст должен быть от 18 до 99 лет.')

class User(AbstractUser):
    username = None  # Убираем поле username

    email = models.EmailField(unique=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(blank=True)
    age = models.IntegerField(validators=[validate_age], null=True)
    gender = models.ForeignKey('Gender', on_delete=models.PROTECT, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True)

    # Уникальные имена для обратных связей
    groups = models.ManyToManyField(Group, related_name='dating_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='dating_user_set', blank=True)

    USERNAME_FIELD = 'email'  # Указываем, что для аутентификации используется email
    REQUIRED_FIELDS = []  # Поля, обязательные для создания пользователя

    def __str__(self):
        return self.email


class Gender(models.Model):
    gen=models.CharField(max_length=6, db_index=True)

    def __str__(self):
        return self.gen