from ckeditor.fields import RichTextField

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Blogger(models.Model):
    """Model representing a blog post author."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    bio = RichTextField(blank=True, null=True)
    profile_pic = models.ImageField(
        null=True, blank=True, upload_to="images/profile/")
    website_url = models.CharField(max_length=200, null=True, blank=True)
    linkedin_url = models.CharField(max_length=200, null=True, blank=True)
    facebook_url = models.CharField(max_length=200, null=True, blank=True)
    twitter_url = models.CharField(max_length=200, null=True, blank=True)
    

    class Meta:
        ordering = ['user', 'bio']

    def get_absolute_url(self):
        """Returns the url to access a particular blogger."""
        return reverse('posts-by-author', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('posts-by-category', args=[str(self.id)])


class Post(models.Model):
    """Model representing a blog post."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Blogger, on_delete=models.CASCADE, null=True)
    header_image = models.ImageField(
        null=True, blank=True, upload_to="images/")
    description = RichTextField(blank=True, null=True)
    post_date = models.DateTimeField(default=timezone.localtime)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    category = models.ManyToManyField(Category)

    def total_likes(self):
        return self.likes.count()

    def get_categories(self):
        categories = [category.name for category in self.category.all()]
        return categories

    def get_absolute_url(self):
        """Returns the url to access a particular blog post."""
        return reverse('post-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.title


class Comment(models.Model):
    """Model representing a comment on a blog post."""
    description = RichTextField(blank=True, null=True)
    post_date = models.DateTimeField(default=timezone.localtime)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    likes = models.ManyToManyField(User, related_name='comment_likes')
    liked = models.BooleanField(null=True)

    class Meta:
        ordering = ['post_date']

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        """Returns the url to access a particular blog post."""
        return reverse('post-detail', args=[str(self.post.id)])

    def __str__(self):
        """String for representing the Model object."""
        len_title = 50
        if len(self.description) > len_title:
            titlestring = self.description[:len_title] + "..."
        else:
            titlestring = self.description
        return titlestring


class Report(models.Model):
    """Model representing a user report about a blog post."""
    subject = models.CharField(max_length=50)
    description = models.TextField(
        max_length=400,
        help_text="Enter your problem here.")
    sender_email = models.EmailField(max_length=50)
    report_date = models.DateTimeField(default=timezone.localtime)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['report_date']

    def __str__(self):
        """String for representing the Model object."""
        return self.subject
