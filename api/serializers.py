from rest_framework import serializers
from home.models import Category, Topic,Post,Comment,PostLike,CommentLike,CommentReply
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('username',)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=('id','name','description')


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model=Topic
        fields=('id','subject',)

    def validate_subject(self,value):
         if Topic.objects.filter(subject=value).exists():
            raise serializers.ValidationError("Topic already Exists")
         return value



class CreatePostSerializer(serializers.ModelSerializer):
    topic=TopicSerializer(required=False)
    class Meta:
        model=Post
        fields=('topic','title','message')



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields=('id','title','message')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=('id','message')


class PostLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model=PostLike
        fields=('liked_by',)


    '''
    name = serializers.SerializerMethodField('get_users_name',required=False)

    def get_users_name(self, obj):
        return obj.liked_by.username
    '''

class CommentLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model=CommentLike
        fields=('comment_liked_by',)


class ReplyCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=CommentReply
        fields=('id','reply_message','replied_by')




