# Generated by Django 2.0.1 on 2018-01-24 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0004_auto_20180123_0227'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='section',
            options={'ordering': ['order_id']},
        ),
        migrations.AddField(
            model_name='section',
            name='order_id',
            field=models.PositiveSmallIntegerField(default=0, help_text='Order wiki sections menu', unique=True),
        ),
    ]
