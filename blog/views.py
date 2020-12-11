from django.shortcuts import render
from django.views import generic
from .models import Blogger, Blog, BlogComment
from django.contrib.auth.models import User

def index(request):
    """View function for home page of site."""

    num_bloggers = Blogger.objects.all().count()
    num_blogs = Blog.objects.all().count()   
    total_comments = BlogComment.objects.all().count()
    
    context = {
        'num_bloggers': num_bloggers,
        'num_blogs': num_blogs,
        'total_comments': total_comments,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class BlogListView(generic.ListView):
    """Generic class-based view for a list of all blogs."""
    model = Blog
    paginate_by = 5
