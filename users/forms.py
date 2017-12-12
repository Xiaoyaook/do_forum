from django import forms
import re

from .models import MyUser


class RegisterForm(forms.Form):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    username = forms.CharField(label="用户名", min_length=4, max_length=16,
                               required=True, )
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='重复密码', widget=forms.PasswordInput, required=True)
    email = forms.EmailField(label="邮箱", max_length=255, required=True)

    def clean_password2(self):
        # 检查密码是否相等
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_username(self):
        username = self.cleaned_data.get("username").strip()
        if not re.match(r"^[a-zA-Z0-9_.]+$", username):
            raise forms.ValidationError("用户名只支持字母、数字、下划线")

        if username[:1] == '_':
            raise forms.ValidationError("用户名不能以下划线打头")

        try:
            MyUser._default_manager.get(username=username)  # _default_manager代表Model的默认管理器,文档地址
        except MyUser.DoesNotExist:                         # https://docs.djangoproject.com/en/2.0/topics/db/managers/
            return username

        raise forms.ValidationError("用户名 {} 已经存在".format(username))

    def clean_email(self):
        email = self.cleaned_data.get("email").strip()

        try:
            MyUser._default_manager.get(email=email)
        except MyUser.DoesNotExist:
            return email

        raise forms.ValidationError(u"邮箱 %s 已经存在" % email)


class LoginForm(forms.Form):
    """登录表单"""
    username = forms.CharField(label="用户名",
                               required=True,)
    password = forms.CharField(label="密码", widget=forms.PasswordInput(), required=True)

    def clean_username(self):
        username = self.cleaned_data.get("username").strip()
        username_not_exist = True
        email_not_exits = True
        try:
            MyUser._default_manager.get(username=username)
        except MyUser.DoesNotExist:
            username_not_exist = False
        try:
            MyUser._default_manager.get(email=username)
        except MyUser.DoesNotExist:
            email_not_exits = False

        print(email_not_exits, username_not_exist)

        if username_not_exist or email_not_exits:
            return username

        raise forms.ValidationError("用户名或邮箱不存在")


class ProfileForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    # password = ReadOnlyPasswordHashField()
    email = forms.EmailField(label="邮箱", required=True, max_length=255,
                             widget=forms.TextInput(attrs={
                                 'class': 'disabled form-control',
                             }))
    profile = forms.CharField(label="个人简介", max_length=140, required=False,
                              widget=forms.Textarea(attrs={'class': 'form-control'}))
    location = forms.CharField(label="城市", max_length=10, required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        user = kwargs.pop('instance', None)
        self.new_email = user.email  # 允许变更Email地址

    class Meta:
        model = MyUser
        fields = ('email', 'profile', 'location')
        # exclude属性告诉 Django 哪些不要放在form中
        # exclude = ('is_active', 'is_admin', 'password', 'last_login',
        #           'date_joined', 'email_verified', 'username', 'avatar',
        #           'last_ip', 'comment_num', 'topic_num')

    def clean_email(self):
        cleaned_data = super(ProfileForm, self).clean()

        email = cleaned_data.get("email").strip()

        try:
            user = MyUser.objects.get(email=email)
        except (MyUser.DoesNotExist, ValueError):
            return email
        else:
            if user.email == self.new_email:
                return email
            else:
                raise forms.ValidationError("邮箱{}已经存在".format(email))


class PasswordChangeForm(forms.Form):
    """改密码"""
    old_password = forms.CharField(label="原密码", widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
    password = forms.CharField(label="新密码", min_length=6, max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
    password2 = forms.CharField(label="重复密码", min_length=6, max_length=30,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("两次密码不相同")

        return password2
