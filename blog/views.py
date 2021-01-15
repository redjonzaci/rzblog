from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import CreateView

from .forms import CreateForm
from .models import Blog, BlogComment, Blogger


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


def LikeView(request, pk):
    blog = get_object_or_404(Blog, id=request.POST.get('blog_id'))
    blog.likes.add(request.user)
    return HttpResponseRedirect(reverse('blog-detail', args=[str(pk)]))


class BlogListView(generic.ListView):
    """Generic class-based view for a list of all blogs."""
    model = Blog
    paginate_by = 5


class BlogDetailView(generic.DetailView):
    """Generic class-based detail view for blog post."""
    model = Blog

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_post = get_object_or_404(Blog, id=self.kwargs['pk'])
        total_likes = current_post.total_likes()
        context['total_likes'] = total_likes
        return context


class BloggerListView(generic.ListView):
    """Generic class-based view for a list of all bloggers."""
    model = Blogger


class BlogListByAuthorView(generic.ListView):
    """Generic class-based view for a list of blogs by a particular blogger."""
    model = Blog
    paginate_by = 5
    template_name = 'blog/blog_list_by_author.html'

    def get_queryset(self):
        """
        Return list of Blog objects by Blogger (author id specified in URL)
        """
        id = self.kwargs['pk']
        target_blogger = get_object_or_404(Blogger, pk=id)
        return Blog.objects.filter(author=target_blogger)

    def get_context_data(self, **kwargs):
        """Add Blogger to context so they can be displayed in the template"""
        # Call the base implementation first to get a context
        context = super(BlogListByAuthorView, self).get_context_data(**kwargs)
        # Get the blogger object from the "pk" URL parameter and add it to the
        # context
        context['blogger'] = get_object_or_404(Blogger, pk=self.kwargs['pk'])
        return context


class BlogCommentCreate(LoginRequiredMixin, CreateView):
    """Form for adding a blog comment. Requires login. """
    model = BlogComment
    fields = ['description', ]

    def get_context_data(self, **kwargs):
        """
        Add associated blog to form template so can display its title in HTML.
        """
        # Call the base implementation first to get a context
        context = super(BlogCommentCreate, self).get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['blog'] = get_object_or_404(Blog, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        """
        Add author and associated blog to form data
        before setting it as valid (so it is saved to model)
        """
        # Add logged-in user as author of comment
        form.instance.author = self.request.user
        # Associate comment with blog based on passed id
        form.instance.blog = get_object_or_404(Blog, pk=self.kwargs['pk'])
        # Call super-class form validation behaviour
        return super(BlogCommentCreate, self).form_valid(form)

    def get_success_url(self):
        """
        After posting comment return to associated blog.
        """
        return reverse('blog-detail', kwargs={'pk': self.kwargs['pk'], })


class BlogPostCreate(LoginRequiredMixin, CreateView):
    """Form for adding a blog post. Requires login. """
    model = Blog
    form_class = CreateForm
    template_name = "blog/add_post.html"

    def form_valid(self, form):
        blog = form.save(commit=False)
        blog.author = Blogger.objects.get(user=self.request.user)
        blog.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """
        After posting comment return to associated blog.
        """
        return reverse('blogs')
