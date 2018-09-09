from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import truncatewords

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):                                                                            # method for getting absolute url
        return '/{0}'.format(self.id)

    def get_posts_count(self):
        return Post.objects.filter(topic__category=self).count()                                              # return total post filter by board

    def get_last_post(self):
        return Post.objects.filter(topic__category=self).order_by('-created_at').first()                      # return last post object


class Topic(models.Model):
    subject = models.CharField(max_length=200)
    last_updated = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='topics')
    starter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topics')
    views = models.PositiveIntegerField(default=0, null=True)

    def __str__(self):
        return self.subject


class Post(models.Model):
    title = models.CharField(max_length=500, null=True)
    message = models.TextField(max_length=4000, help_text='Maximum 4000 words')
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE,related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', null=True)

    def __str__(self):
        return truncatewords(self.message, 10)

    @property
    def short_description(self):
        return truncatewords(self.message, 10)


class Comment(models.Model):
    message = models.TextField(max_length=4000, help_text='Maximum 4000 words')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(null=True)
    created_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    updated_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', null=True)

    def __str__(self):
        return self.message


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_likes')
    comment_liked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_likes')

class CommentReply(models.Model):
    reply_message = models.TextField(max_length = 2000,null = True)
    comment = models.ForeignKey(Comment, on_delete = models.CASCADE, related_name = 'comment_replies')
    replied_by=models.ForeignKey(User, on_delete = models.CASCADE, related_name= 'comment_replies')
    reply_time = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return truncatewords(self.reply_message,10)





