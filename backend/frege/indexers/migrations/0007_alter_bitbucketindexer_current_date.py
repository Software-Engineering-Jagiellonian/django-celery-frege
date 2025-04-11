# Generated by Django 5.1.7 on 2025-04-10 20:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indexers', '0006_gitlabindexer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bitbucketindexer',
            name='current_date',
            field=models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0, tzinfo=datetime.timezone.utc), help_text='The creation date of repository from which to start searching. Please note that Bitbucket API paginates repos by creation date, so the dates are used to iterate over repositories.', verbose_name='current date'),
        ),
    ]
