from django.contrib import admin
from .models import Category, Topic, Post, CommentReply, Comment

# Register your models here.


admin.site.register(Category)
admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(CommentReply)
admin.site.register(Comment)
