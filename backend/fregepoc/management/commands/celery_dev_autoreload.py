import shlex
import subprocess

from django.core.management.base import BaseCommand
from django.utils import autoreload

# Taken from:
# https://medium.com/aubergine-solutions/auto-reload-development-mode-for-celery-worker-using-docker-compose-and-django-management-2ba8e313eb37  # noqa: E501


def restart_celery(*args, **kwargs):
    kill_worker_cmd = "pkill -9 celery"
    subprocess.call(shlex.split(kill_worker_cmd))
    start_worker_cmd = "celery -A fregepoc worker -l info"
    subprocess.call(shlex.split(start_worker_cmd))


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Starting celery worker with autoreload...")
        autoreload.run_with_reloader(restart_celery, args=None, kwargs=None)
