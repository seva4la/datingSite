from tkinter import Image

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import ForeignKey, PROTECT
import uuid


def validate_age(value):
    if value < 18 or value > 99:
        raise ValidationError('Возраст должен быть от 18 до 99 лет.')

class User(models.Model):
    # email=
    # password=
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30)
    description = models.TextField (blank=True)
    age = models.IntegerField(validators=[validate_age])
    gender = ForeignKey('Gender', on_delete=PROTECT)
    # profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.name


class Gender(models.Model):
    gen=models.CharField(max_length=6, db_index=True)

    def __str__(self):
        return self.gen