import sys
import time
from django.core.management.base import BaseCommand
from django.conf import settings
from frege.repositories.tasks.task_profiling import create_repos_task
from celery.result import AsyncResult

class Command(BaseCommand):
    help = 'Describe what your command does here'

    def handle(self, *args, **options):
      # Start the initial task
      task_result = create_repos_task.apply_async()
      print(f'Initial task started, ID: {task_result.id}. Waiting for summarize task...')

      # Wait for the creation task to complete and get summary task id
      summarize_task_id = task_result.get()  # This will block until the task completes
      
      # Monitoring summarize task
      summarize_task = AsyncResult(summarize_task_id)
      spinner = ['|', '/', '-', '\\']
      idx = 0
      message = f"Waiting for summarize task to complete... "
      total_length = len(message) + 1;
      while not summarize_task.ready():
          
          sys.stdout.write(f"\r{message}{spinner[idx % len(spinner)]}")
          sys.stdout.flush()
          idx += 1
          time.sleep(1)
      sys.stdout.write("\r" + " " * total_length + "\r")
      sys.stdout.flush()
      print()
      print("----------------------------")

      if summarize_task.successful():
        response = summarize_task.get()  # Retrieve the summarize_task if successful
        self.stdout.write(self.style.SUCCESS(response))
        print("----------------------------")
        print()
      else:
        try:
            summarize_task.get()  # This will raise the exception captured by Celery if the task failed
        except ValueError as e:
            self.stdout.write(self.style.ERROR('Error from summarize task: ' + str(e)))
        except Exception as e:
            self.stdout.write(self.style.ERROR('Unexpected error: ' + str(e)))
