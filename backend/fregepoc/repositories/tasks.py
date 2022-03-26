import os

import git
from celery import shared_task
from celery.signals import celeryd_init
from django.conf import settings
from django.utils import timezone
from github import Github

from fregepoc import celery_app as app
from fregepoc.repositories.analyzers.base import AnalyzerFactory
from fregepoc.repositories.constants import ProgrammingLanguages

from fregepoc.repositories.models import Repository, RepositoryFile

# TODO: switch to proper logging instead of printing
# TODO: should probably move aux functions somewhere else


def _get_repo_local_path(repo):
    return os.path.join(settings.DOWNLOAD_PATH, repo.name)


# TODO: quick hack, clean this out
def _get_repo_files(repo_obj):
    for file_path in repo_obj.git.ls_files().split("\n"):
        if file_path.endswith(".py"):
            yield file_path, ProgrammingLanguages.PYTHON
        elif file_path.endswith((".cpp", ".hpp")):
            yield file_path, ProgrammingLanguages.CPP


def _finalize_repo_analysis(repo_obj):
    if all(repo_obj.files.all().values_list("analyzed", flat=True)):
        repo_obj.analyzed = True
        repo_obj.save()
        print(
            f"Repository {repo_obj.git_url} fully analyzed, "
            "deleting files from disk..."
        )
        repo_local_path = _get_repo_local_path(repo_obj)
        os.system(f"rm -rf {repo_local_path}")


@celeryd_init.connect
def init_worker(**kwargs):
    crawl_repos_task.delay()


@shared_task
def crawl_repos_task():
    # TODO: crawler & dispatcher might need to be merged to allow
    #       us to determine if we've hit a throttling limit or not
    # TODO: switch between using ssh and https when having tokens available
    # TODO: use envs to set query parameters

    min_forks = 100
    min_stars = 100

    github_token = os.environ.get("GITHUB_TOKEN")
    g = Github(github_token) if github_token else Github()
    # TODO: save last known page, increase query result page size - current
    #       approach is very hacky & mb. let the range be adjustable
    for page in range(5000):
        list_of_repos = g.search_repositories(
            query=f"forks:>={min_forks} stars:>={min_stars} is:public",
            sort="stars",
            page=page,
        )

        repos_to_process = [Repository(
                    name=repo.name,
                    description=repo.description,
                    git_url=repo.clone_url,
                    repo_url=repo.html_url,
                    commit_hash=repo.get_branch(repo.default_branch).commit.sha,
                ) for repo in list_of_repos]
        Repository.objects.bulk_create(repos_to_process)
        for repo in repos_to_process:
            process_repo_task.delay(repo.id)


@shared_task
def process_repo_task(repo_id):
    # TODO: docstring & cleanup

    try:
        repo = Repository.objects.get(id=repo_id)
    except Repository.DoesNotExist:
        print("process_repo_task >>> repo does not exist")
        return

    repo_local_path = _get_repo_local_path(repo)
    print(f"process_repo_task >>> fetching repo via url: {repo.git_url}")

    try:
        repo_obj = git.Repo.clone_from(repo.git_url, repo_local_path)
        repo.fetch_time = timezone.now()
        repo.save()
        print("process_repo_task >>> repo cloned")
    except git.exc.GitCommandError:
        try:
            repo_obj = git.Repo(repo_local_path)
            print("process_repo_task >>> repo already exists, fetched from disk")
        except git.exc.NoSuchPathError:
            print(
                "process_repo_task >>> tried fetching from disk, "
                "but repo does not exist"
            )
            return

    repo_files = [
        RepositoryFile(
            repository=repo,
            repo_relative_file_path=relative_file_path,
            language=language,
            analyzed=False,
        )
        for relative_file_path, language in _get_repo_files(repo_obj)
    ]
    RepositoryFile.objects.bulk_create(repo_files)

    for repo_file in repo_files:
        analyze_file_task.delay(repo_file.id)
    else:
        _finalize_repo_analysis(repo)


@shared_task
def analyze_file_task(repo_file_id):
    # TODO: docstring & cleanup

    try:
        repo_file = RepositoryFile.objects.get(id=repo_file_id)
    except RepositoryFile.DoesNotExist:
        print("analyze_file_task >>> repo_file does not exist")
        return

    analyzers = AnalyzerFactory.make_analyzers(repo_file.language)
    if not analyzers:
        repo_file.delete()
        return

    file_abs_path = os.path.join(
        _get_repo_local_path(repo_file.repository), repo_file.repo_relative_file_path
    )
    with open(file_abs_path, "r") as f:
        for analyzer in analyzers:
            metrics_dict = analyzer.analyze(f.read())

    repo_file.metrics = metrics_dict
    repo_file.analyzed = True
    repo_file.analysed_time = timezone.now()
    repo_file.save()

    print(f"analyze_file_task >>> repo_file {repo_file.repository.name} analyzed")
    _finalize_repo_analysis(repo_file.repository)
