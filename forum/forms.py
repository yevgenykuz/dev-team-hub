from ckeditor.widgets import CKEditorWidget
from django import forms
from forum.models import Topic, Post


class NewTopicForm(forms.ModelForm):
    body = forms.CharField(
        widget=CKEditorWidget(),
        max_length=5000,
        help_text='The max length of the text is 5000.'
    )

    class Meta:
        model = Topic
        fields = ['subject', 'body']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['body', ]
