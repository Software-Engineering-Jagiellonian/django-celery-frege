from fregepoc import celery_app as app
from constants import extension_to_analyzer
import git
import os

# TODO: add a proper logger


@app.task
def crawl_repos_task(crawler):
    # TODO: crawl repos using provided crawler class, dispatching
    #       processors as it goes

    # TODO: crawler & dispatcher might need to be merged to allow
    #       us to discern if we hit a throttling limit or not

    # TODO: switch between using ssh and https when having tokens available
    pass


@app.task
def process_repo_task(url):
    # TODO: docstring & cleanup

    url = 'https://github.com/Software-Engineering-Jagiellonian/frege-git-repository-analyzer.git'
    repo_path = '/tmp/' + os.path.basename(url).split('.')[0]
    print(f'process_repo_task >>> url provided: {url}')

    try:
        repo = git.Repo.clone_from(url, repo_path)
    except git.exc.GitCommandError:
        repo = git.Repo(repo_path)

    for file_path in repo.git.ls_files().split('\n'):
        ext = file_path.split('.')[-1]
        try:
            analyze_file_task.delay(
                file_path,
                extension_to_analyzer[ext])
        except KeyError:
            continue


@app.task
def analyze_file_task(file_path, analyzer):
    # TODO: use the analyzer provided, dump data to database,
    #       delete repo files if all files were analyzed
    print(f'analyze_file_task >>> {file_path}, {analyzer}')