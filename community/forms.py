from django import forms
from .models import Topic, Comment


class ReplyForm(forms.ModelForm):
    content = forms.CharField(label='回复', required=False)

    def clean_content(self):
        content = self.cleaned_data.get("content").strip()
        if len(content) == 0:
            raise forms.ValidationError("请输入评论内容...")
            # elif len(content) < 5:
            # raise forms.ValidationError("评论内容太短哦...")
        elif len(content) > 800:
            raise forms.ValidationError("评论内容太长哦...")
        else:
            return content

    class Meta:
        model = Comment
        fields = ['content', ]
