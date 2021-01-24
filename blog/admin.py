from django.contrib import admin

from .models import Blog, BlogComment, Blogger, Report

admin.site.register(Blogger)
# admin.site.register(Blog)
admin.site.register(BlogComment)
admin.site.register(Report)


class BlogCommentsInline(admin.TabularInline):
    model = BlogComment


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    inlines = [BlogCommentsInline]
