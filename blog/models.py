from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Blogger(models.Model):
    """Model representing a blog author."""
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    bio = models.TextField(max_length=400, help_text="Enter your bio details here.")

    class Meta:
        ordering = ['user', 'bio']
    
    def get_absolute_url(self):
        """Returns the url to access a particular blogger."""
        return reverse('blogs-by-author', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.user.username


class Blog(models.Model):
    """Model representing a blog post."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Blogger, on_delete=models.SET_NULL, null=True)
    header_image = models.ImageField(null=True, blank=True, upload_to="images/")
    description = models.TextField(max_length=2000, help_text="Enter your blog text here.")
    post_date = models.DateTimeField(default=timezone.localtime)

    class Meta:
        ordering = ['-post_date']

    def get_absolute_url(self):
        """Returns the url to access a particular blog post."""
        return reverse('blog-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.title


class BlogComment(models.Model):
    """Model representing a comment on a blog post."""
    description = models.TextField(max_length=400, help_text="Enter your comment here.")
    post_date = models.DateTimeField(default=timezone.localtime)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    class Meta:
        ordering = ['post_date']

    def __str__(self):
        """String for representing the Model object."""
        len_title=50
        if len(self.description) > len_title:
            titlestring = self.description[:len_title] + "..."
        else:
            titlestring = self.description
        return titlestring
