# Generated by Django 2.2 on 2021-02-06 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_comment_liked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='liked',
            field=models.BooleanField(null=True),
        ),
    ]