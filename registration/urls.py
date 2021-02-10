from django.urls import path

from blog import views as blog_views

from . import views

urlpatterns = [
    path(
        'register/',
        views.UserRegisterView.as_view(),
        name='register'
    ),
    path(
        'blogger/create/',
        blog_views.BloggerCreate.as_view(),
        name='blogger-create'
    ),
]
