from django.urls import path

from . import views

urlpatterns = [
    path(
        '',
        views.index,
        name='index'),
    path(
        'blogs/',
        views.BlogListView.as_view(),
        name='blogs'),
    path(
        'blog/<int:pk>',
        views.BlogDetailView.as_view(),
        name='blog-detail'),
    path(
        'bloggers/',
        views.BloggerListView.as_view(),
        name='bloggers'),
    path(
        'blogger/<int:pk>',
        views.BlogListByAuthorView.as_view(),
        name='blogs-by-author'),
    path(
        'blog/<int:pk>/comment/',
        views.BlogCommentCreate.as_view(),
        name='blog_comment'),
    path(
        'blog/add_post/',
        views.BlogPostCreate.as_view(),
        name='add_post'),
    path(
        'like/<int:pk>',
        views.LikeView,
        name='like_post'),
    path(
        'edit/<int:pk>',
        views.BlogPostUpdate.as_view(),
        name='edit_post'),
]
