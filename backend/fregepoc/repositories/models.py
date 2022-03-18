import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


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
        help_text=_("The time when the repository has got downloaded."),
    )
