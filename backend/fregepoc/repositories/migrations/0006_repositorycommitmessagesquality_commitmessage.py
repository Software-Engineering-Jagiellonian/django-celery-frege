# Generated by Django 4.0.10 on 2023-06-29 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repositories', '0005_repositoryfile_average_cyclomatic_complexity_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RepositoryCommitMessagesQuality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('analyzed', models.BooleanField(default=False, help_text='Whether the repository commit messages quality has been analyzed or not.', verbose_name='Analyzed')),
                ('commits_amount', models.IntegerField(default=0, help_text='Amount of commits in repository', verbose_name='commits amount')),
                ('average_commit_message_characters_length', models.DecimalField(decimal_places=2, default=0, help_text='Average word length of commit message', max_digits=10, verbose_name='average commit message characters length')),
                ('average_commit_message_words_amount', models.DecimalField(decimal_places=2, default=0, help_text='Average word length of commit message', max_digits=10, verbose_name='average word length')),
                ('average_commit_message_fog_index', models.DecimalField(decimal_places=2, default=0, help_text='Average fog index value of commit message', max_digits=10, verbose_name='average commit message fog index')),
                ('classifiable_to_unclassifiable_commit_messages_ratio', models.DecimalField(decimal_places=2, default=0, help_text='Ratio of meaningful to non-meaningful commit messages in repository', max_digits=10, verbose_name='classifiable to unclassifiable commit messages ratio')),
                ('percentage_of_feature_commits', models.DecimalField(decimal_places=2, default=0, help_text='Percentage of feature commits in repository', max_digits=10, verbose_name='percentage of feature commits')),
                ('percentage_of_fix_commits', models.DecimalField(decimal_places=2, default=0, help_text='Percentage of fix commits in repository', max_digits=10, verbose_name='percentage of fix commits')),
                ('percentage_of_config_change_commits', models.DecimalField(decimal_places=2, default=0, help_text='Percentage of config change commits in repository', max_digits=10, verbose_name='percentage of config change commits')),
                ('percentage_of_merge_pr_commits', models.DecimalField(decimal_places=2, default=0, help_text='Percentage of merge pull request commits in repository', max_digits=10, verbose_name='percentage of merge pr commits')),
                ('percentage_of_unclassified_commits', models.DecimalField(decimal_places=2, default=0, help_text='Percentage of unclassified commits in repository', max_digits=10, verbose_name='percentage of unclassified commits')),
                ('repository', models.ForeignKey(help_text='The repository that this commit message belongs to.', on_delete=django.db.models.deletion.CASCADE, related_name='repository_commit_messages_quality', to='repositories.repository')),
            ],
            options={
                'verbose_name_plural': 'Repositories Commit Messages Quality',
            },
        ),
        migrations.CreateModel(
            name='CommitMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('analyzed', models.BooleanField(default=False, help_text='Whether the commit message has been analyzed or not.', verbose_name='Analyzed')),
                ('analyzed_time', models.DateTimeField(auto_now_add=True, help_text='The time when the commit message was analyzed.', verbose_name='analyzed time')),
                ('author', models.CharField(help_text='The author of the commit', max_length=255, verbose_name='Commit author')),
                ('commit_hash', models.CharField(help_text='The hash of the analyzed commit.', max_length=40, verbose_name='commit hash')),
                ('message', models.TextField(help_text='Entire commit message text', verbose_name='message')),
                ('commit_type', models.CharField(choices=[('FEATURE', 'Feature'), ('FIX', 'Fix'), ('CONFIG CHANGE', 'Config'), ('MERGE PR', 'Merge Pr'), ('UNCLASSIFIED', 'Unclassified')], default='UNCLASSIFIED', help_text='Commit type based on commit message content.', max_length=40, verbose_name='commit type')),
                ('commit_message_char_length', models.IntegerField(default=0, help_text='Length of commit message in number of characters', verbose_name='commit message char length')),
                ('words_amount', models.IntegerField(default=0, help_text='Amount of words in commit message', verbose_name='words amount')),
                ('average_word_length', models.DecimalField(decimal_places=2, default=0, help_text='Average word length of commit message', max_digits=10, verbose_name='average word length')),
                ('fog_index', models.DecimalField(decimal_places=2, default=0, help_text='Gunning Fog index value for commit message', max_digits=10, verbose_name='fog index')),
                ('repository', models.ForeignKey(help_text='The repository that this commit message belongs to.', on_delete=django.db.models.deletion.CASCADE, related_name='commit_messages', to='repositories.repository')),
            ],
            options={
                'verbose_name_plural': 'Commit Messages',
            },
        ),
    ]
