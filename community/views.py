from django.shortcuts import render, get_object_or_404
from .models import Boards, Topic, Category, Comment
from .forms import ReplyForm


def index(request):
    """首页"""
    boards = Boards.objects.all()

    return render(request, 'community/index.html', context={
        'boards': boards
    })


def board(request, board_name):  # 接受一个board_name参数,该参数由Board中定义的方法传入
    """板块"""
    topics = Topic.objects.filter(boards__name=board_name)
    return render(request, 'community/board.html', context={
        'board_name': board_name,
        'topics': topics
    })


def topic(request, pk):
    """帖子"""
    post = get_object_or_404(Topic, pk=pk)
    comments = Comment.objects.filter(topic__pk=pk).order_by('created_time')
    return render(request, 'community/topic.html', context={
        'post': post,
        'comments': comments
    })


def reply(request, pk):  # 评论，需要登录
    """评论"""
    post = get_object_or_404(Topic, pk=pk)
    comments = Comment.objects.filter(topic__pk=pk).order_by('created_time')

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)  # call save() with commit=False, then it will return an object
            #  that hasn’t yet been saved to the database
            comment.topic = post  # 把comment与文章关联
            comment.author = request.user  # 这里先放着，等先完成用户系统
            comment.save()
    else:
        form = ReplyForm()

    return render(request, 'community/topic.html', context={
        'post': post,
        'comments': comments,
        'form': form
    })

