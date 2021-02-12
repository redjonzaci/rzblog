from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
from rzblog import settings

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
        'add_post/',
        views.PostCreate.as_view(),
        name='add_post'),
    path(
        'like/<int:pk>',
        views.like_post,
        name='like_post'),
    path(
        'edit/<int:pk>',
        views.PostUpdate.as_view(),
        name='edit_post'),
    path(
        '<int:pk>/delete/',
        views.PostDelete.as_view(),
        name='delete_post'),
    path(
        'bloggers/',
        views.BloggerListView.as_view(),
        name='bloggers'),
    path(
        'blogger/<int:pk>',
        views.PostListByAuthorView.as_view(),
        name='posts-by-author'),
    path(
        'blogger/<int:pk>/profile/',
        views.BloggerUpdate.as_view(),
        name='edit_blogger'),
    path(
        'post/<int:pk>/comment/',
        views.CommentCreate.as_view(),
        name='comment'),
    path(
        'post/<int:pk>/comment/edit/',
        views.CommentUpdate.as_view(),
        name='edit_comment'),
    path(
        'post/<int:pk>/comment/delete/',
        views.CommentDelete.as_view(),
        name='delete_comment'),
    path(
        'post/<int:pk>/report/',
        views.ReportCreate.as_view(),
        name='report_post'),
    path(
        'report/success/',
        views.success,
        name='success'),
    path(
        'comment/like/<int:pk>',
        views.like_comment,
        name='like_comment'),
    path(
        'categories/',
        views.CategoryListView.as_view(),
        name='categories'),
    path(
        'category/<int:pk>',
        views.PostListByCategoryView.as_view(),
        name='posts-by-category'),
    path(
        'add_category/',
        views.CategoryCreate.as_view(),
        name='add_category')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
