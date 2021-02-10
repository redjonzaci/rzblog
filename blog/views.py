from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from diyblog import settings

from .forms import CreateForm, ReportForm
from .models import Blogger, Category, Comment, Post, Report


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

    return render(request, 'index.html', context=context)


# Post SECTION
class PostListView(generic.ListView):
    """Generic class-based view for a list of all blog posts."""
    model = Post
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        context = {'post_list': Post.objects.annotate(
            like_count=Count('likes')).order_by('-like_count')}
        return context


class PostDetailView(generic.DetailView):
    """Generic class-based detail view for blog post."""
    model = Post

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_post = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = current_post.total_likes()
        liked = False
        if current_post.likes.filter(id=self.request.user.id).exists():
            liked = True
        context['total_likes'] = total_likes
        context['liked'] = liked
        for comment in current_post.comment_set.all():
            comment.liked = False
            if comment.likes.filter(id=self.request.user.id).exists():
                comment.liked = True
            comment.save()
            context['comment.liked'] = comment.liked
        context['categories'] = current_post.get_categories()
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    """Form for adding a blog post. Requires login. """
    model = Post
    form_class = CreateForm
    template_name = "blog/add_post.html"

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = Blogger.objects.get(user=self.request.user)
        post.save()
        form.save_m2m()
        return HttpResponseRedirect(reverse('posts'))


class PostUpdate(LoginRequiredMixin, UpdateView):
    """Form for editing a blog post. Requires login of post author. """
    model = Post
    template_name = "blog/edit_post.html"
    fields = ['title', 'header_image', 'description', 'category']

    def get_context_data(self, **kwargs):
        """
        Adds associated post to form template
        so its title can be displayed in HTML.
        """
        # Call the base implementation first to get a context
        context = super(PostUpdate, self).get_context_data(**kwargs)
        # Get the post from id and add it to the context
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context


class PostDelete(LoginRequiredMixin, DeleteView):
    """Form for deleting a blog post. Requires login of post author. """
    model = Post
    template_name = "blog/delete_post.html"
    success_url = reverse_lazy('posts')

    def get_context_data(self, **kwargs):
        """
        Adds associated post to form template
        so its title can be displayed in HTML.
        """
        context = super(PostDelete, self).get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context


def like_post(request, pk):
    """View function to process clicking the like button."""
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


# Blogger SECTION
class BloggerListView(generic.ListView):
    """Generic class-based view for a list of all bloggers."""
    model = Blogger


class PostListByAuthorView(generic.ListView):
    """
    Generic class-based view for a list of posts by a particular blogger.
    """
    model = Post
    paginate_by = 5
    template_name = 'blog/post_list_by_author.html'

    def get_queryset(self):
        """
        Returns list of Post objects by Blogger (author id specified in URL)
        """
        target_blogger = get_object_or_404(Blogger, pk=self.kwargs['pk'])
        return Post.objects.filter(author=target_blogger).annotate(
            like_count=Count('likes')).order_by('-like_count')

    def get_context_data(self, **kwargs):
        """Adds Blogger to context so they can be displayed in the template"""
        context = super(PostListByAuthorView, self).get_context_data(**kwargs)
        context['blogger'] = get_object_or_404(Blogger, pk=self.kwargs['pk'])
        return context


class BloggerCreate(CreateView):
    model = Blogger
    fields = ['bio']

    def form_valid(self, form):
        blogger = form.save(commit=False)
        blogger.user = User.objects.get(username=self.request.user.username)
        blogger.save()
        return HttpResponseRedirect(reverse('bloggers'))


class BloggerUpdate(LoginRequiredMixin, UpdateView):
    """Form for adding a bio to the blogger when registered. """
    model = Blogger
    template_name = 'blog/add_blogger_bio.html'
    fields = ['bio']


# Comment SECTION
class CommentCreate(LoginRequiredMixin, CreateView):
    """Form for adding a comment. Requires login. """
    model = Comment
    fields = ['description']

    def get_context_data(self, **kwargs):
        """
        Adds associated post to form template
        so we can display its title in HTML.
        """
        context = super(CommentCreate, self).get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        """
        Adds author and associated post to form data
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
        After posting comment returns to associated post.
        """
        return reverse('post-detail', kwargs={'pk': self.kwargs['pk'], })


class CommentUpdate(LoginRequiredMixin, UpdateView):
    """
    Form for editing a comment.
    Requires login of comment author.
    """
    model = Comment
    template_name = "blog/edit_comment.html"
    fields = ['description']

    def get_context_data(self, **kwargs):
        """
        Adds associated comment to form template
        so we can display its title in HTML.
        """
        context = super(CommentUpdate, self).get_context_data(**kwargs)
        context['comment'] = get_object_or_404(Comment, pk=self.kwargs['pk'])
        return context


class CommentDelete(LoginRequiredMixin, DeleteView):
    """
    Form for deleting a comment.
    Requires login of comment author.
    """
    model = Comment
    template_name = "blog/delete_comment.html"
    success_url = reverse_lazy('posts')

    def get_context_data(self, **kwargs):
        """
        Adds associated comment to form template
        so can display its title in HTML.
        """
        context = super(CommentDelete, self).get_context_data(**kwargs)
        context['comment'] = get_object_or_404(Comment, pk=self.kwargs['pk'])
        return context


def like_comment(request, pk):
    """View function to process clicking the like button of a comment."""
    comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


# Report SECTION
class ReportCreate(LoginRequiredMixin, CreateView):
    """Form for reporting a blog post. Requires login."""
    model = Report
    form_class = ReportForm
    template_name = "blog/report.html"

    def get_context_data(self, **kwargs):
        """
        Adds associated post to form template
        so we can display its title in HTML.
        """
        context = super(ReportCreate, self).get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        report = form.save(commit=False)
        report.author = self.request.user
        report.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        send_mail(report.subject, report.description,
                  settings.EMAIL_HOST_USER, ['redi.z1908@gmail.com'],
                  fail_silently=False)
        report.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('success')


def success(request):
    return render(request, 'blog/success.html')


# Category SECTION
class CategoryListView(generic.ListView):
    """Generic class-based view for a list of all categories."""
    model = Category


class PostListByCategoryView(generic.ListView):
    """
    Generic class-based view for a list of posts of a category.
    """
    model = Post
    template_name = 'blog/post_list_by_category.html'

    def get_queryset(self):
        """
        Returns list of Post objects by Category
        ordered by like count (category id specified in URL)
        """
        target_category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return Post.objects.filter(category=target_category).annotate(
            like_count=Count('likes')).order_by('-like_count')

    def get_context_data(self, **kwargs):
        """Adds category to context so they can be displayed in the template"""
        context = super(
            PostListByCategoryView,
            self).get_context_data(
            **kwargs)
        context['category'] = get_object_or_404(Category, pk=self.kwargs['pk'])
        return context


class CategoryCreate(LoginRequiredMixin, CreateView):
    """Form for adding a category. Requires login. """
    model = Category
    template_name = "blog/add_category.html"
    fields = ['name']
    success_url = reverse_lazy('categories')
