from django.shortcuts import render, redirect
from users.forms import RegisterForm, LoginForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages

from users.models import MyUser, Friendship
from community.models import Topic, Comment


@csrf_protect  # 只在这里加入decorator进行csrf防护是不被推荐的,所以我们同时还在template中使用csrf_token tag.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)  # 用提交来的数据,实例化一个用户注册表单

        if form.is_valid():
            data = form.clean()
            new_user = MyUser.objects.create_user(username=data["username"],
                                                  email=data["email"],
                                                  password=data["password"])  # 调用UserManager的方法,注册用户
            form.save()  # 调用表单的 save 方法将用户数据保存到数据库
            # 之后加入邮箱验证,和注册后自动登录
            return redirect('/')  # 注册成功，跳转回首页
    else:
        form = RegisterForm()

    # 渲染模板
    # 如果用户正在访问注册页面，则渲染的是一个空的注册表单
    # 如果用户通过表单提交注册信息，但是数据验证不合法，则渲染的是一个带有错误信息的表单
    return render(request, 'users/register.html', context={'form': form})


def login(request):
    # 之后添加功能:如果用户已经登录,重定向
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.clean()
            username = data['username']
            if '@' in username:  # 邮箱也可以登录
                email = username
            else:
                user = MyUser.objects.get(username=username)
                email = user.email

            user = authenticate(email=email, password=data['password'])
            if user is not None:
                auth_login(request, user)
                # 这里还可以更进一步的写,这里先简单的重定向
                return redirect('/')  # 登录成功，跳转回首页
            else:
                messages.error(request, '密码不正确！')
                return render(request, 'users/login.html', context={'form': form})
                # use an explicit context_dictionary, instead of passing locals()
    else:
        form = LoginForm()

        return render(request, 'users/login.html', {
            'form': form
        })


def logout(request):  # 登出
    auth_logout(request)
    return redirect('/')


def user(request, uid):  # 用户的个人页面
    user_from_id = MyUser.objects.get(pk=uid)  # 可以是别人访问也可以是自己访问
    visitor = request.user  # Authentication中间件给每个HttpRequest对象添加user属性,代表当前登陆的用户
    friend = None
    if visitor.is_authenticated():
        try:
            friend = Friendship.objects.filter(from_friend=visitor, to_friend=user_from_id).first()
        except (MyUser.DoesNotExist, Friendship.DoesNotExist):
            friend = None

    topic_list = Topic.objects.order_by('-created_on').filter(author=user_from_id.id)[:10]
    comment_list = Comment.objects.order_by('-created_on').filter(author=user_from_id)[:10]
    return render(request, 'users/user.html', context={
        'friend': friend,
        'topic_list': topic_list,
        'comment_list': comment_list
    })


# 用户个人页面 - 所有帖子
def user_topics(request, uid):
    this_user = MyUser.objects.get(pk=uid)
    topic_list = Topic.objects.order_by('-created_on').filter(author=uid)
    # 之后可以对所有帖子进行一个分页

    return render(request, 'users/user_topics.html', context={
        'this_user': this_user,
        'topic_list': topic_list
    })


# 用户个人页面 - 所有回复
def user_comments(request, uid):
    this_user = MyUser.objects.get(pk=uid)
    comment_list = Comment.objects.order_by("-created_on").filter(author=uid)
    # 分页

    return render(request, 'users/user_topics.html', context={
        'this_user': this_user,
        'comment_list': comment_list
    })


@login_required
@csrf_protect
def send_verified_email(request):  # 发送验证邮件
    pass


def email_verified(request, uid, token):  # 邮箱验证
    pass


def find_password(request):  # 找回密码
    pass


def first_reset_password(request, uid=None, token=None):
    pass


def reset_password(request):
    pass