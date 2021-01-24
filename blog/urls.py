from django.urls import path

from . import views

urlpatterns = [
    path(
        '',
        views.index,
        name='index'),
    path(
        'posts/',
        views.PostListView.as_view(),
        name='posts'),
    path(
        'post/<int:pk>',
        views.PostDetailView.as_view(),
        name='post-detail'),
    path(
        'bloggers/',
        views.BloggerListView.as_view(),
        name='bloggers'),
    path(
        'blogger/<int:pk>',
        views.PostListByAuthorView.as_view(),
        name='posts-by-author'),
    path(
        'post/<int:pk>/comment/',
        views.CommentCreate.as_view(),
        name='comment'),
    path(
        'add_post/',
        views.PostCreate.as_view(),
        name='add_post'),
    path(
        'like/<int:pk>',
        views.LikeView,
        name='like_post'),
    path(
        'edit/<int:pk>',
        views.PostUpdate.as_view(),
        name='edit_post'),
]
