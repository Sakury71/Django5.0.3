from django.contrib import admin

from .models import Blog, BlogCategory, BlogComment


# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'pub_time', 'category', 'author']


class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_time']


class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['blog', 'content', 'author', 'pub_time']


admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogCategory, BlogCategoryAdmin)
admin.site.register(BlogComment, BlogCommentAdmin)
