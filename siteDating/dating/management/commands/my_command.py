from django.core.management.base import BaseCommand
from django.utils import timezone
from dating.models import User
from django.contrib.auth.hashers import make_password

class Command (BaseCommand):
    # текст при выводе --help
    help='Создание User'

    def add_arguments(self, parser):
        # указываем сколько и каких аргументов принимает команда
        parser.add_argument('User', nargs=2, type=str)

    def handle(self, *args, **options):
        # прописываем логику
        user_new=User.objects.create(
            email = options['User'][0],
            password = make_password(options['User'][1])
        )
        if user_new:
            self.stdout.write('Successfully created User!')
        else:
            self.stdout.write('NOOOOOO the User has not been created :(')