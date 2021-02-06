from django.contrib import admin

from .models import Blogger, Category, Comment, Post, Report

admin.site.register(Blogger)
# admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Report)
admin.site.register(Category)


class CommentsInline(admin.TabularInline):
    model = Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [CommentsInline]
