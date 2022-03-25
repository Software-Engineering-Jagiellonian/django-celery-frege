from django.db import models
from django.utils.translation import gettext_lazy as _

from fregepoc.repositories.constants import ProgrammingLanguages


class Repository(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Repository name'),
        help_text=_('The name of the repository'),
    )
    description = models.TextField(
        max_length=2048,
        verbose_name=_('Repository description'),
        help_text=_('The description of the repository'),
        blank=True,
        null=True,
    )
    analyzed = models.BooleanField(
        _("Analyzed"),
        default=False,
        help_text="Indicates whether the repository has been analyzed."
    )
    git_url = models.URLField(
        _("git url"), help_text=_("The url used to clone the repository")
    )
    repo_url = models.URLField(
        _("repo url"), help_text=_("The url used to crawl or visit the repository.")
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
            "The time when the repository was discovered. It is set automatically on creation."
        ),
    )
    fetch_time = models.DateTimeField(
        _("fetch time"),
        blank=True,
        null=True,
        help_text=_("The time when the repository was downloaded."),
    )

    def __str__(self):
        return self.name


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
        help_text="Whether the file has been analyzed or not."
    )
    language = models.CharField(
        max_length=20,
        verbose_name=_("programming language"),
        help_text=_("Programming language present in the repository."),
        choices=ProgrammingLanguages.choices,
    )
    repo_relative_file_path = models.FilePathField(
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
    analysed_time = models.DateTimeField(
        _("analysed time"),
        auto_now_add=True,
        help_text=_("The time when the file was analyzed."),
    )
