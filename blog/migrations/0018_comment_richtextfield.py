# Generated by Django 2.2 on 2021-02-11 22:00

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_blogger_richtextfield'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
