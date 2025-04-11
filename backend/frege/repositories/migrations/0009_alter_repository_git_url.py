# Generated by Django 5.1.7 on 2025-04-10 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repositories', '0008_repository_analysis_failed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repository',
            name='git_url',
            field=models.URLField(help_text='The url used to clone the repository', unique=True, verbose_name='git url'),
        ),
    ]
