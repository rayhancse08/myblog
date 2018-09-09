from django.contrib import admin
from .models import Category, Topic, Post, CommentReply

# Register your models here.





admin.site.register(Category)
admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(CommentReply)