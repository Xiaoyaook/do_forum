from django.contrib import admin
from .models import Boards, Category, Topic, Comment


class BoardsAdmin(admin.ModelAdmin):
    list_display = ('name', 'num_topics',)


class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_time', 'updated_time', 'boards', 'author',)
    search_fields = ['title']
    list_filter = ('boards__name',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'topic', 'author', 'created_time',)
    list_filter = ('topic__title',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Boards, BoardsAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)