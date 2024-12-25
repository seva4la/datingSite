from django.db.models import ManyToManyField
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import ForeignKey, PROTECT
import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


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

    groups = models.ManyToManyField(Group, related_name='dating_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='dating_user_set', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    likes = ManyToManyField('self', related_name='liked_by', symmetrical=False, blank=True)

    def like_user(self, other_user):
        if other_user == self:
            return False

        self.likes.add(other_user)

        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            f"user_{other_user.id}_likes",
            {
                "type": "send_like_update",
                "data": {
                    "liked_by": self.id,
                    "liked_by_email": self.email,
                }
            }
        )
        return True

    def __str__(self):
        return self.email


class Gender(models.Model):
    gen=models.CharField(max_length=6, db_index=True)

    def __str__(self):
        return self.gen