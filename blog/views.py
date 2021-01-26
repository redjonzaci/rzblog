from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import CreateForm
from .models import Post, Comment, Blogger


def index(request):
    """View function for home page of site."""

    num_bloggers = Blogger.objects.all().count()
    num_posts = Post.objects.all().count()
    total_comments = Comment.objects.all().count()

    context = {
        'num_bloggers': num_bloggers,
        'num_posts': num_posts,
        'total_comments': total_comments,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


class PostListView(generic.ListView):
    """Generic class-based view for a list of all blog posts."""
    model = Post
    paginate_by = 5


class PostDetailView(generic.DetailView):
    """Generic class-based detail view for blog post."""
    model = Post

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_post = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = current_post.total_likes()
        context['total_likes'] = total_likes
        return context


class BloggerListView(generic.ListView):
    """Generic class-based view for a list of all bloggers."""
    model = Blogger


class PostListByAuthorView(generic.ListView):
    """
    Generic class-based view for a list of blog posts by a particular blogger.
    """
    model = Post
    paginate_by = 5
    template_name = 'blog/blog_list_by_author.html'

    def get_queryset(self):
        """
        Return list of Blog objects by Blogger (author id specified in URL)
        """
        id = self.kwargs['pk']
        target_blogger = get_object_or_404(Blogger, pk=id)
        return Post.objects.filter(author=target_blogger)

    def get_context_data(self, **kwargs):
        """Add Blogger to context so they can be displayed in the template"""
        # Call the base implementation first to get a context
        context = super(PostListByAuthorView, self).get_context_data(**kwargs)
        # Get the blogger object from the "pk" URL parameter and add it to the
        # context
        context['blogger'] = get_object_or_404(Blogger, pk=self.kwargs['pk'])
        return context


class CommentCreate(LoginRequiredMixin, CreateView):
    """Form for adding a blog comment. Requires login. """
    model = Comment
    fields = ['description', ]

    def get_context_data(self, **kwargs):
        """
        Add associated blog to form template so can display its title in HTML.
        """
        # Call the base implementation first to get a context
        context = super(CommentCreate, self).get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        """
        Add author and associated blog to form data
        before setting it as valid (so it is saved to model)
        """
        # Add logged-in user as author of comment
        form.instance.author = self.request.user
        # Associate comment with blog based on passed id
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        # Call super-class form validation behaviour
        return super(CommentCreate, self).form_valid(form)

    def get_success_url(self):
        """
        After posting comment return to associated blog.
        """
        return reverse('post-detail', kwargs={'pk': self.kwargs['pk'], })


class PostCreate(LoginRequiredMixin, CreateView):
    """Form for adding a blog post. Requires login. """
    model = Post
    form_class = CreateForm
    template_name = "blog/add_post.html"

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = Blogger.objects.get(user=self.request.user)
        post.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """
        After posting the blog post return to the list of blogs.
        """
        return reverse('posts')


class PostUpdate(LoginRequiredMixin, UpdateView):
    """Form for editing a blog post. Requires login of post author. """
    model = Post
    template_name = "blog/edit_post.html"
    fields = ['title', 'description', ]


class PostDelete(LoginRequiredMixin, DeleteView):
    """Form for deleting a blog post. Requires login of post author. """
    model = Post
    template_name = "blog/delete_post.html"
    success_url = reverse_lazy('posts')


class CommentUpdate(LoginRequiredMixin, UpdateView):
    """
    Form for editing a blog post comment.
    Requires login of comment author.
    """
    model = Comment
    template_name = "blog/edit_comment.html"
    fields = ['description', ]


class CommentDelete(LoginRequiredMixin, DeleteView):
    """
    Form for deleting a blog post comment.
    Requires login of comment author.
    """
    model = Comment
    template_name = "blog/delete_comment.html"
    success_url = reverse_lazy('posts')
