from django import forms
from .models import Category, Topic, Post, Comment, CommentReply
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class TopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'What is your mind?'}

        ),
        max_length=2000,
        help_text='Maximum 200 words'
    )

    class Meta:
        model = Topic
        fields = ['subject', 'message']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'message', ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message', ]


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = CommentReply
        fields = ['reply_message']


