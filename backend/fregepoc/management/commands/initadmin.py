from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
import os


# Taken from: https://stackoverflow.com/questions/39744593/how-to-create-a-django-superuser-if-it-doesnt-exist-non-interactively
class Command(BaseCommand):
    help = "Creates an admin user non-interactively if it doesn't exist"

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            help="Admin's username",
            default=os.environ.get('DJANGO_SUPERUSER_USERNAME'))
        parser.add_argument(
            '--email',
            help="Admin's email",
            default=os.environ.get('DJANGO_SUPERUSER_EMAIL'))
        parser.add_argument(
            '--password',
            help="Admin's password",
            default=os.environ.get('DJANGO_SUPERUSER_PASSWORD'))

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username=options['username']).exists():
            User.objects.create_superuser(
                username=options['username'],
                email=options['email'],
                password=options['password'])
