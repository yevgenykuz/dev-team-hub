# Generated by Django 2.0.1 on 2018-01-25 07:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0008_auto_20180125_0417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='favorite_by',
            field=models.ManyToManyField(blank=True, help_text='A list of users that marked this entry as their favorite', to=settings.AUTH_USER_MODEL),
        ),
    ]
