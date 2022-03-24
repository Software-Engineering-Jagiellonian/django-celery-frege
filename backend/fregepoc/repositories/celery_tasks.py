from fregepoc.repositories.constants import (
    extension_to_analyzer,
    ProgrammingLanguages)
from fregepoc.repositories.models import Repository, RepositoryFile
from django.utils import timezone
from django.conf import settings
from fregepoc import celery_app as app
import git
import os

# TODO: switch to proper logging instead of printing
# TODO: should probably move aux functions somewhere else


def _get_repo_local_path(repo):
    return os.path.join(settings.DOWNLOAD_PATH, repo.name)


def _get_repo_files(repo_obj):
    for file_path in repo_obj.git.ls_files().split('\n'):
        if file_path.endswith('.py'):
            yield file_path, ProgrammingLanguages.PYTHON


def _finalize_repo_analysis(repo_obj):
    if all(repo_obj.files.all().values_list('analyzed', flat=True)):
        repo_obj.analyzed = True
        repo_obj.save()
        print(f'Repository {repo_obj.git_url} fully analyzed, '
              'deleting files from disk...')
        repo_local_path = _get_repo_local_path(repo_obj)
        os.system(f'rm -rf {repo_local_path}')


@app.task
def crawl_repos_task(crawler):
    # TODO: crawl repos using provided crawler class, dispatching
    #       processors as it goes

    # TODO: crawler & dispatcher might need to be merged to allow
    #       us to determine if we've hit a throttling limit or not

    # TODO: switch between using ssh and https when having tokens available
    url = 'https://github.com/Software-Engineering-Jagiellonian/frege-git-repository-analyzer.git'

    # TODO: this will most likely be converted to bulk_create
    repo_name = os.path.basename(url).split('.')[0]
    repo = Repository.objects.create(
        name=repo_name,
        git_url=url,
        repo_url=url,
        commit_hash='master')

    process_repo_task.delay(repo.id)


@app.task
def process_repo_task(repo_id):
    # TODO: docstring & cleanup

    try:
        repo = Repository.objects.get(id=repo_id)
    except Repository.DoesNotExist:
        print('process_repo_task >>> repo does not exist')
        return

    repo_local_path = _get_repo_local_path(repo)
    print(f'process_repo_task >>> fetching repo via url: {repo.git_url}')

    try:
        repo_obj = git.Repo.clone_from(repo.git_url, repo_local_path)
        repo.fetch_time = timezone.now()
        repo.save()
    except git.exc.GitCommandError:
        # repo already exists, trying to fetch from disk
        repo_obj = git.Repo(repo_local_path)

    repo_files = [
        RepositoryFile(
            repository=repo,
            repo_relative_file_path=relative_file_path,
            language=language,
            analyzed=False
        ) for relative_file_path, language in _get_repo_files(repo_obj)]
    RepositoryFile.objects.bulk_create(repo_files)

    for repo_file in repo_files:
        analyze_file_task.delay(repo_file.id)


@app.task
def analyze_file_task(repo_file_id):
    # TODO: use the analyzer provided, dump data to database,
    #       delete repo if all files were analyzed

    try:
        repo_file = RepositoryFile.objects.get(id=repo_file_id)
    except RepositoryFile.DoesNotExist:
        print('analyze_file_task >>> repo_file does not exist')
        return

    try:
        analyzer = extension_to_analyzer[repo_file.language]
    except KeyError:
        print('analyze_file_task >>> analyzer not found '
              f'(lang: {repo_file.language})')
        return

    file_abs_path = os.path.join(
        _get_repo_local_path(repo_file.repository),
        repo_file.repo_relative_file_path)
    with open(file_abs_path, 'r') as f:
        metrics_dict = analyzer.analyze(f.read())

    repo_file.metrics = metrics_dict
    repo_file.analyzed = True
    repo_file.analysed_time = timezone.now()
    repo_file.save()

    print(f'repo_file {os.path.basename(repo_file.repo_relative_file_path)} analyzed')
    _finalize_repo_analysis(repo_file.repository)
