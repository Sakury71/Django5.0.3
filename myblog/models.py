from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class BlogCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name='分类名称')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_time']
        verbose_name = '博客分类'
        verbose_name_plural = verbose_name


class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    pub_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, verbose_name='分类')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='发布者')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pub_time']
        verbose_name = '博客内容'
        verbose_name_plural = verbose_name


class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments', verbose_name='博客')
    content = models.TextField(verbose_name='内容')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                               verbose_name='评论者')
    pub_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-pub_time']
        verbose_name = '博客评论'
        verbose_name_plural = verbose_name
