# Generated by Django 2.0.1 on 2018-01-25 01:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_article_published'),
        ('hub', '0010_siteconfig_current_release_release_notes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='siteconfig',
            name='current_release_release_notes',
        ),
        migrations.AddField(
            model_name='siteconfig',
            name='current_release_notes',
            field=models.ForeignKey(help_text='Link to release notes article', null=True, on_delete=django.db.models.deletion.SET_NULL, to='news.Article'),
        ),
    ]
