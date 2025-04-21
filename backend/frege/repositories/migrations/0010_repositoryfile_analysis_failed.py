from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repositories', '0009_alter_repository_git_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='repositoryfile',
            name='analysis_failed',
            field=models.BooleanField(help_text='Whether the file analysis was successful.', default=False),
        ),
    ]
