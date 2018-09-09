from django import forms
from .models import Category, Topic, Post, Comment, CommentReply
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def clean(self):
        form_data=self.cleaned_data
        if User.objects.filter(username=form_data['username']).exists():
            forms.ValidationError("*** User already exists")

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    def clean(self):
        form_data=self.cleaned_data
        if Category.objects.filter(name=form_data['name']).exists():
            forms.ValidationError("*** Category already exists")


class TopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'What is your mind?'}

        ),
        max_length=2000,
        help_text='Maximum 200 words'
    )
    title=forms.CharField(widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'What is your mind?'}

        ),
        max_length=2000,
        help_text='Maximum 200 words')
    class Meta:
        model = Topic
        fields = ['subject', 'title','message']

    def clean_subject(self):
        subject=self.cleaned_data['subject']
        if Topic.objects.filter(subject=subject).exists():
            raise forms.ValidationError('***Topic already Exists')
        return subject



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


