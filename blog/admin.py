from django.contrib import admin

from .models import Post, Comment, Blogger, Report

admin.site.register(Blogger)
# admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Report)


class CommentsInline(admin.TabularInline):
    model = Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [CommentsInline]
