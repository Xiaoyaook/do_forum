from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone

import hashlib
import random
import string


SALT = 'aliang'  # 给验证token加盐,最好从setting文件中引入，这里直接硬写了


class UserManager(BaseUserManager):  # 用户创建
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, username and password.
        """
        if not email:
            raise ValueError('邮箱是必须的哦')
        if not username:
            raise ValueError('用户名是必须的哦')
        now = timezone.now()
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            date_joined=now,
            last_login=now,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email,username and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='邮箱',
        max_length=255,
        unique=True,
    )
    username = models.CharField("用户名", max_length=16, unique=True)
    date_joined = models.DateTimeField("用户注册时间", default=timezone.now)

    location = models.CharField("城市", max_length=10, blank=True)
    profile = models.CharField("个人简介", max_length=140, blank=True)
    avatar = models.CharField("头像", max_length=128, blank=True)

    last_ip = models.GenericIPAddressField("上次访问IP", default="0.0.0.0")

    email_verified = models.BooleanField("邮箱是否验证", default=False)

    topic_num = models.IntegerField("帖子数", default=0)
    comment_num = models.IntegerField("评论数", default=0)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()  # 用户注册模型

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def is_email_verified(self):
        return self.email_verified

    def get_username(self):
        return self.username

    def get_email(self):
        return self.email

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Friendship(models.Model):
    """
    关系表Friendship实现关注功能,字段field分别是 粉丝和关注，并且Foreignkey为MyUser
    """
    from_friend = models.ForeignKey(MyUser, related_name='friend_set')  # 粉丝
    to_friend = models.ForeignKey(MyUser, related_name='to_friend_set')  # 关注
    date_followed = models.DateTimeField(default=timezone.now)


class EmailVerified(models.Model):
    user = models.OneToOneField(MyUser, related_name="user")
    token = models.CharField("Email 验证 token", max_length=32, default=None)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{}@{}".format(self.user, self.token)

    def generate_token(self):
        year = self.timestamp.year
        month = self.timestamp.month
        day = self.timestamp.day
        date = "%s-%s-%s" % (year, month, day)
        token = hashlib.md5(str(self.user.id) + self.user.username + self.ran_str() + date).hexdigest()
        return token

    def ran_str(self):
        salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        return salt + SALT


class FindPass(models.Model):  # 找回密码
    user = models.OneToOneField(MyUser, verbose_name="用户")
    token = models.CharField(max_length=32, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}@{}".format(self.user, self.token)

    def generate_token(self):
        year = self.timestamp.year
        month = self.timestamp.month
        day = self.timestamp.day
        date = "%s-%s-%s" % (year, month, day)
        token = hashlib.md5(str(self.user.id)+self.user.username+self.ran_str()+date).hexdigest()
        return token

    def ran_str(self):
        salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        return salt + SALT
