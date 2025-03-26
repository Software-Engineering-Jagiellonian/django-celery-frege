from django.db import models
from django.utils.translation import gettext_lazy as _

from frege.repositories.constants import ProgrammingLanguages, CommitMessagesTypes


class Repository(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Repository name"),
        help_text=_("The name of the repository"),
    )
    description = models.TextField(
        max_length=2048,
        verbose_name=_("Repository description"),
        help_text=_("The description of the repository"),
        blank=True,
    )
    analyzed = models.BooleanField(
        _("Analyzed"),
        default=False,
        help_text="Indicates whether the repository has been analyzed.",
    )
    git_url = models.URLField(
        _("git url"), help_text=_("The url used to clone the repository")
    )
    repo_url = models.URLField(
        _("repo url"),
        help_text=_("The url used to crawl or visit the repository."),
    )
    commit_hash = models.CharField(
        max_length=40,
        verbose_name=_("commit hash"),
        help_text=_("The commit hash actual at the time of crawling."),
    )
    discovered_time = models.DateTimeField(
        _("discovered time"),
        auto_now_add=True,
        help_text=_(
            "The time when the repository was discovered. "
            "It is set automatically on creation."
        ),
    )
    fetch_time = models.DateTimeField(
        _("fetch time"),
        blank=True,
        null=True,
        help_text=_("The time when the repository was downloaded."),
    )
    analyzed_time = models.DateTimeField(
        _("analyzed time"),
        blank=True,
        null=True,
        help_text=_("The time when the repository was analyzed."),
    )

    clone_failed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _("Repositories")


class RepositoryFile(models.Model):
    repository = models.ForeignKey(
        Repository,
        on_delete=models.CASCADE,
        related_name="files",
        help_text=_("The repository that this file belongs to."),
    )
    analyzed = models.BooleanField(
        _("Analyzed"),
        default=False,
        help_text="Whether the file has been analyzed or not.",
    )
    language = models.CharField(
        max_length=20,
        verbose_name=_("programming language"),
        help_text=_("Programming language present in the repository."),
        choices=ProgrammingLanguages.choices,
    )
    repo_relative_file_path = models.CharField(  # noqa: DJ01
        max_length=512,
        blank=True,
        null=True,
        help_text=_("File path, relative to the repository root."),
    )
    metrics = models.JSONField(
        _("metrics"),
        blank=True,
        null=True,
        help_text=_("The metrics of the file."),
    )
    analyzed_time = models.DateTimeField(
        _("analyzed time"),
        auto_now_add=True,
        help_text=_("The time when the file was analyzed."),
    )
    lines_of_code = models.FloatField(
        blank=True,
        null=True,
        help_text=_("Total lines of code in file"),
    )
    token_count = models.FloatField(
        blank=True,
        null=True,
        help_text=_("token count in file"),
    )
    function_count = models.FloatField(
        blank=True,
        null=True,
        help_text=_("number of functions in file"),
    )
    average_function_name_length = models.FloatField(
        blank=True,
        null=True,
        help_text=_("average function name length in file"),
    )
    average_lines_of_code = models.FloatField(
        blank=True,
        null=True,
        help_text=_("average lines of code"),
    )
    average_token_count = models.FloatField(
        blank=True,
        null=True,
        help_text=_("average token count"),
    )
    average_cyclomatic_complexity = models.FloatField(
        blank=True,
        null=True,
        help_text=_("average cyclomatic complexity of file"),
    )
    average_parameter_count = models.FloatField(
        blank=True,
        null=True,
        help_text=_("average parameter count"),
    )

    def __str__(self):
        return f"file: {self.repository.name}/{self.repo_relative_file_path}"


class RepositoryCommitMessagesQuality(models.Model):

    repository = models.ForeignKey(
        Repository,
        on_delete=models.CASCADE,
        related_name="repository_commit_messages_quality",
        help_text=_("The repository that this commit message belongs to."),
    )

    analyzed = models.BooleanField(
        _("Analyzed"),
        default=False,
        help_text="Whether the repository commit messages quality has been analyzed or not.",
    )

    commits_amount = models.IntegerField(
        verbose_name=_("commits amount"),
        help_text=_("Amount of commits in repository"),
        default=0,
    )

    average_commit_message_characters_length = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        verbose_name=_("average commit message characters length"),
        help_text=_("Average word length of commit message"),
        default=0,
    )

    average_commit_message_words_amount = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        verbose_name=_("average word length"),
        help_text=_("Average word length of commit message"),
        default=0,
    )

    average_commit_message_fog_index = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        verbose_name=_("average commit message fog index"),
        help_text=_("Average fog index value of commit message"),
        default=0,
    )

    classifiable_to_unclassifiable_commit_messages_ratio = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        verbose_name=_("classifiable to unclassifiable commit messages ratio"),
        help_text=_("Ratio of meaningful to non-meaningful commit messages in repository"),
        default=0,
    )

    percentage_of_feature_commits = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        verbose_name=_("percentage of feature commits"),
        help_text=_("Percentage of feature commits in repository"),
        default=0,
    )

    percentage_of_fix_commits = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        verbose_name=_("percentage of fix commits"),
        help_text=_("Percentage of fix commits in repository"),
        default=0,
    )

    percentage_of_config_change_commits = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        verbose_name=_("percentage of config change commits"),
        help_text=_("Percentage of config change commits in repository"),
        default=0,
    )

    percentage_of_merge_pr_commits = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        verbose_name=_("percentage of merge pr commits"),
        help_text=_("Percentage of merge pull request commits in repository"),
        default=0,
    )

    percentage_of_unclassified_commits = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        verbose_name=_("percentage of unclassified commits"),
        help_text=_("Percentage of unclassified commits in repository"),
        default=0,
    )

    class Meta:
        verbose_name_plural = _("Repositories Commit Messages Quality")


class CommitMessage(models.Model):

    repository = models.ForeignKey(
        Repository,
        on_delete=models.CASCADE,
        related_name="commit_messages",
        help_text=_("The repository that this commit message belongs to."),
    )

    analyzed = models.BooleanField(
        _("Analyzed"),
        default=False,
        help_text="Whether the commit message has been analyzed or not.",
    )

    analyzed_time = models.DateTimeField(
        _("analyzed time"),
        auto_now_add=True,
        help_text=_("The time when the commit message was analyzed."),
    )

    author = models.CharField(
        max_length=255,
        verbose_name=_("Commit author"),
        help_text=_("The author of the commit"),
    )

    commit_hash = models.CharField(
        max_length=40,
        verbose_name=_("commit hash"),
        help_text=_("The hash of the analyzed commit."),
    )

    message = models.TextField(
        verbose_name=_("message"),
        help_text="Entire commit message text"
    )

    commit_type = models.CharField(
        max_length=40,
        verbose_name=_("commit type"),
        help_text=_("Commit type based on commit message content."),
        choices=CommitMessagesTypes.choices,
        default=CommitMessagesTypes.UNCLASSIFIED
    )

    commit_message_char_length = models.IntegerField(
        verbose_name=_("commit message char length"),
        help_text=_("Length of commit message in number of characters"),
        default=0,
    )

    words_amount = models.IntegerField(
        verbose_name=_("words amount"),
        help_text=_("Amount of words in commit message"),
        default=0,
    )

    average_word_length = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        verbose_name=_("average word length"),
        help_text=_("Average word length of commit message"),
        default=0,
    )

    fog_index = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        verbose_name=_("fog index"),
        help_text=_("Gunning Fog index value for commit message"),
        default=0,
    )

    class Meta:
        verbose_name_plural = _("Commit Messages")
