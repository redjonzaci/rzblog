# Generated by Django 2.2 on 2021-01-24 21:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0005_blog_likes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=50)),
                ('description', models.TextField(help_text='Enter your problem here.', max_length=400)),
                ('sender_email', models.EmailField(max_length=50)),
                ('report_date', models.DateTimeField(default=django.utils.timezone.localtime)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Blog')),
            ],
            options={
                'ordering': ['report_date'],
            },
        ),
    ]
