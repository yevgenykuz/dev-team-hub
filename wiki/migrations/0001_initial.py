# Generated by Django 2.0.1 on 2018-01-27 05:45

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The key/title/name of an actual field.', max_length=200)),
                ('slug', models.SlugField(editable=False, max_length=255, unique=True)),
                ('value', ckeditor.fields.RichTextField(help_text='The value/body/textual data of this field.', max_length=20000)),
                ('order_id', models.PositiveSmallIntegerField(default=0, help_text="The presentation order of this field in the 'block' that holds field of this type on a wiki page, relative to other fields of the same type.")),
            ],
            options={
                'ordering': ['type__order_id', 'order_id', 'slug'],
            },
        ),
        migrations.CreateModel(
            name='CustomFieldType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='A meaningful name.', max_length=200, unique=True)),
                ('slug', models.SlugField(editable=False, max_length=255, unique=True)),
                ('name_plural', models.CharField(help_text="The title of the 'block' in the wiki entry page that holds fields of this custom type.", max_length=255)),
                ('description', models.TextField(help_text='How should custom fields of this type look like?', max_length=2500)),
                ('order_id', models.PositiveSmallIntegerField(default=0, help_text="The presentation order of this custom field type 'block' in a wiki entry page, relative to other custom field type 'blocks'.")),
            ],
            options={
                'ordering': ['order_id', 'slug'],
            },
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The title of this wiki entry (page).', max_length=200, unique=True)),
                ('slug', models.SlugField(editable=False, max_length=255, unique=True)),
                ('publish', models.BooleanField(default=False)),
                ('value', ckeditor.fields.RichTextField(blank=True, help_text='The body of this wiki entry, without custom fields. Displayed above the custom fields in the wiki page.', max_length=20000)),
                ('order_id', models.PositiveSmallIntegerField(default=0, help_text='The presentation order in wiki section page, relative to other entries of this type.')),
                ('custom_fields', models.ManyToManyField(blank=True, help_text="Add fields to a 'block' off a custom field type. The presentation order (that is determined by the order id of the fields) will be shown on the right after saving.", to='wiki.CustomField')),
                ('custom_fields_presentation_order', models.ManyToManyField(blank=True, help_text="Add custom field types 'blocks' to this page. The presentation order (that is determined by the order id of the types) will be shown onthe right after saving.", to='wiki.CustomFieldType')),
                ('favorite_by', models.ManyToManyField(blank=True, help_text='A list of users that marked this entry as their favorite will be shown on the right. Use to see how popular an entry is.', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'entries',
                'ordering': ['section__order_id', 'order_id', 'slug'],
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of a wiki section/category.', max_length=200, unique=True)),
                ('slug', models.SlugField(editable=False, max_length=255, unique=True)),
                ('description', models.TextField(help_text='What entries should this wiki section hold?', max_length=2500)),
                ('order_id', models.PositiveSmallIntegerField(default=0, help_text='The presentation order in the wiki sections menu, relative to other wiki sections.')),
            ],
            options={
                'ordering': ['order_id', 'slug'],
            },
        ),
        migrations.AddField(
            model_name='entry',
            name='section',
            field=models.ForeignKey(help_text='The wiki section to which this entry belongs.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='wiki.Section'),
        ),
        migrations.AddField(
            model_name='customfield',
            name='type',
            field=models.ForeignKey(help_text='The type of this field.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='wiki.CustomFieldType'),
        ),
    ]
