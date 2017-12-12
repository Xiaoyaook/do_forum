from django.db import models
# from django.contrib.auth.models import User
from django.urls import reverse

from forum.settings import AUTH_USER_MODEL


# 论坛板块
class Boards(models.Model):
    name = models.CharField(max_length=100)
    num_topics = models.IntegerField(default=0)  # 主题数

    def get_absolute_url(self):
        return reverse('community:board', kwargs={'board_name': self.name})

    def __str__(self):  # 美化打印出来的结果
        return self.name

"""
class Tag(models.Model):
    name = models.CharField(max_length=100)
"""


# 类别
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):  # 美化打印出来的结果
        return self.name


# 帖子
class Topic(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(blank=True, null=True)

    boards = models.ForeignKey(Boards)  # 这个外键必然存在,暂时不需要其他参数
    author = models.ForeignKey(AUTH_USER_MODEL)  # 因为我们没使用默认的USER,所以应该指向settings.AUTH_USER_MODEL

    category = models.ManyToManyField(Category, blank=True)  # 帖子类型

    def get_absolute_url(self):  # 关键字传参
        return reverse('community:topic', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['created_time']

        def __str__(self):  # 美化打印出来的结果
            return self.title


# 评论
class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(AUTH_USER_MODEL)  # 因为我们没使用默认的USER,所以应该指向settings.AUTH_USER_MODEL
    topic = models.ForeignKey(Topic)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # 美化打印出来的结果
        return self.content
