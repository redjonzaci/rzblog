from django.contrib import admin
from .models import Blogger, Blog, BlogComment

admin.site.register(Blogger)
# admin.site.register(Blog)
admin.site.register(BlogComment)

class BlogCommentsInline(admin.TabularInline):
    model = BlogComment

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    inlines = [BlogCommentsInline]
