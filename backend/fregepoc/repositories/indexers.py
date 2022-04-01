from github import Github
from collections.abc import Iterator


# NOTE: this file is meant to be split into a folder with files representing analyzers


class BaseIndexer():
    pass


# class GitHubIndexer(Indexer):
#     BASE_API_URL = 'https://gitlab.com/api/v4/projects'

#     def __init__(self, indexer_type: IndexerType, rabbitmq_parameters: RabbitMQConnectionParameters,
#                  database_parameters: DatabaseConnectionParameters, rejected_publish_delay: int,
#                  github_indexer_parameters: GitHubIndexerParameters):
#         super().__init__(indexer_type, rabbitmq_parameters, database_parameters, rejected_publish_delay)

#         self.github_indexer_parameters = github_indexer_parameters
#         if github_indexer_parameters.github_personal_token:
#             self.g = Github(github_indexer_parameters.github_personal_token)
#         else:
#             self.g = Github()

#         self.iter = self.__get_next_repo()

#     def __get_next_repo(self):
#         min_stars = self.github_indexer_parameters.min_stars
#         min_forks = self.github_indexer_parameters.min_forks
#         last_updated = self.github_indexer_parameters.last_updated

#         for page in range(5000):

#             while True:
#                 try:
#                     list_of_repos = self.g.search_repositories(query=f'forks:>={min_forks} stars:>={min_stars}'
#                                                                      f' is:public pushed:>={last_updated}',
#                                                                sort='stars', page=page)
#                     break
#                 except github.GithubException as e:
#                     print("because of limitations of github-api, system will wait for 30 min")
#                     time.sleep(60 * 30)

#             for repo in list_of_repos:
#                 languages = {}
#                 while True:
#                     try:
#                         for x in repo.get_languages().keys():
#                             y = LANGUAGES.get(x, False)
#                             if y:
#                                 languages[Language(y)] = True
#                         break
#                     except github.GithubException as e:
#                         print("because of limitations of github-api, system will wait for 30 min")
#                         time.sleep(60 * 30 )

#                 if not len(languages):
#                     continue

#                 yield CrawlResult(
#                     id=str(repo.id),
#                     repo_url=repo.clone_url,
#                     git_url=repo.html_url,
#                     languages=languages
#                 )

#     def crawl_next_repository(self, prev_repository_id: Optional[str]) -> Optional[CrawlResult]:
#         self.log.debug('Start a new crawl')
#         return next(self.iter)
