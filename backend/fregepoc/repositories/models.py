import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from fregepoc.repositories.constants import ProgrammingLanguages


class Repository(models.Model):
    id = models.UUIDField(_("ID"), primary_key=True, default=uuid.uuid4, editable=False)
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
    crawl_time = models.DateTimeField(
        _("crawl time"),
        auto_now_add=True,
        help_text=_(
            "The time when the repository was discovered. It is set automatically on creation."
        ),
    )
    download_time = models.DateTimeField(
        _("download time"),
        blank=True,
        null=True,
        help_text=_("The time when the repository was downloaded."),
    )


class RepositoryLanguage(models.Model):
    language = models.CharField(
        max_length=20,
        verbose_name=_("programming language"),
        help_text=_("Programming language present in the repository."),
        choices=ProgrammingLanguages.choices,
    )
    analyzed = models.BooleanField(
        _("analyzed"),
        help_text=_(
            "Whether the repository has been analyzed with regard to this language."
        ),
        default=False,
    )
    repository = models.ForeignKey(
        Repository,
        on_delete=models.CASCADE,
        related_name="programming_languages",
        verbose_name=_("repository"),
        help_text=_("The related repository."),
    )


class RepositoryLanguageFile(models.Model):
    repository_language = models.ForeignKey(
        RepositoryLanguage,
        on_delete=models.CASCADE,
        related_name="files",
        verbose_name=_("source code files"),
        help_text=_("The source code."),
    )
    file_path = models.FilePathField(
        path=settings.DOWNLOAD_PATH,
    )
