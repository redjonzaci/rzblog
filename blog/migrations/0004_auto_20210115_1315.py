# Generated by Django 2.2 on 2021-01-15 12:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20201213_0001'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='header_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='post_date',
            field=models.DateTimeField(default=django.utils.timezone.localtime),
        ),
        migrations.AlterField(
            model_name='blogcomment',
            name='post_date',
            field=models.DateTimeField(default=django.utils.timezone.localtime),
        ),
    ]
