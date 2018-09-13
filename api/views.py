from django.shortcuts import render
from rest_framework.generics import ListAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView,CreateAPIView
from .serializers import CategorySerializer,CreatePostSerializer,TopicSerializer,PostSerializer,CommentSerializer,PostLikeSerializer,CommentLikeSerializer,ReplyCommentSerializer
from home.models import Category, Topic,Post,PostLike,Comment,CommentLike,CommentReply
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

# Create your views here.


class CategoryAPIViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (IsAdminUser,)



class CreateTopicAPIView(CreateAPIView):
    serializer_class = CreatePostSerializer

    def post(self, request, *args, **kwargs):
        category = Category.objects.get(pk=self.kwargs['pk'])
        serializer = CreatePostSerializer(data=request.data)
        if serializer.is_valid():

            topic = Topic()
                #objects.create(subject=serializer.validated_data['topic'], category=category,
            topic_dict= serializer.validated_data['topic']                           #starter=self.request.user)
            topic.subject=topic_dict['subject']
            topic.category=category
            topic.starter=self.request.user
            topic.save()

            Post.objects.create(
                title=serializer.validated_data['title'],
                message=serializer.validated_data.get('message'),
                topic=topic,
                created_by=request.user
            )
        return Response("Topic Created")



class TopicAPIViewSet(viewsets.ModelViewSet):
    serializer_class = TopicSerializer
    lookup_url_kwarg = 'topic_pk'

    def get_queryset(self):
        category = get_object_or_404(Category,pk=self.kwargs['pk'])
        queryset=category.topics.all()
        return queryset

    def perform_create(self, serializer):
        category = get_object_or_404(Category, id=self.kwargs['pk'])
        serializer.save(starter=self.request.user, category=category)

    def destroy(self, request, *args, **kwargs):
        topic=get_object_or_404(Topic,pk=self.kwargs['topic_pk'])
        if not request.user==topic.starter:
            return Response("Not allowed.Only owner can delete")
        return super().destroy(request,*args,**kwargs)

    def update(self, request, *args, **kwargs):
        topic = get_object_or_404(Topic, pk=self.kwargs['topic_pk'])
        if not request.user == topic.starter:
            return Response("Not allowed.Only owner can update")
        return super().update(request, *args, **kwargs)



class PostAPIViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    lookup_url_kwarg = 'post_pk'

    def get_queryset(self):
        topic = get_object_or_404(Topic, id=self.kwargs['topic_pk'], category=self.kwargs['pk'])
        queryset = topic.posts.all()
        return queryset

    def perform_create(self, serializer):
        topic = get_object_or_404(Topic, id=self.kwargs['topic_pk'], category=self.kwargs['pk'])
        serializer.save(created_by=self.request.user, topic=topic)

    def destroy(self, request, *args, **kwargs):
        post=get_object_or_404(Post,pk=self.kwargs['post_pk'])
        if not request.user==post.created_by:
            return Response("Not allowed.Only owner can delete")
        return super().destroy(request,*args,**kwargs)

    def update(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        if not request.user == post.created_by:
            return Response("Not allowed.Only owner can update")
        return super().update(request, *args, **kwargs)




class CommentAPIViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'comment_pk'


    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs['post_pk'], topic=self.kwargs['topic_pk'])
        queryset = post.comments.all()
        return queryset

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['post_pk'], topic=self.kwargs['topic_pk'])
        serializer.save(created_user=self.request.user, post=post)

    def destroy(self, request, *args, **kwargs):
        comment=get_object_or_404(Comment,pk=self.kwargs['comment_pk'])
        if not request.user==comment.created_user:
            return Response("Not allowed.Only owner can delete")
        return super().destroy(request,*args,**kwargs)

    def update(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs['comment_pk'])
        if not request.user == comment.created_user:
            return Response("Not allowed.Only owner can update")
        return super().update(request, *args, **kwargs)


class PostLikeAPIView(ListCreateAPIView):
    serializer_class = PostLikeSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs['post_pk'], topic=self.kwargs['topic_pk'])
        queryset = post.likes.all()
        return queryset

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        already_liked = PostLike.objects.filter(liked_by=self.request.user,post=post)
        if already_liked:
            already_liked.delete()
            return Response("Unlike")
        else:
           serializer.save(liked_by=self.request.user, post=post)
           return Response("post created")



class CommentLikeAPIView(ListCreateAPIView):
    serializer_class = CommentLikeSerializer
    def get_queryset(self):
        comment = get_object_or_404(Comment, id=self.kwargs['comment_pk'], post=self.kwargs['post_pk'])
        queryset = comment.comment_likes.all()
        return queryset

    def perform_create(self, serializer):
        comment = get_object_or_404(Comment, pk=self.kwargs['comment_pk'])
        already_liked = CommentLike.objects.filter(comment_liked_by=self.request.user,comment=comment)
        if already_liked:
            already_liked.delete()
            return Response("Unlike")
        else:
           serializer.save(comment_liked_by=self.request.user, comment=comment)
           return Response("post created")


class ReplyCommentAPIViewSet(viewsets.ModelViewSet):
    serializer_class = ReplyCommentSerializer
    lookup_url_kwarg = 'reply_comment_pk'

    def get_queryset(self):
        comment = get_object_or_404(Comment, id=self.kwargs['comment_pk'])
        queryset = comment.comment_replies.all()
        return queryset

    def perform_create(self, serializer):
        comment = get_object_or_404(Comment, id=self.kwargs['comment_pk'])
        serializer.save(replied_by=self.request.user, comment=comment)

    def destroy(self, request, *args, **kwargs):
        reply_comment=get_object_or_404(CommentReply,pk=self.kwargs['reply_comment_pk'])
        if not request.user==reply_comment.replied_by:
            return Response("Not allowed.Only owner can delete reply.")
        return super().destroy(request,*args,**kwargs)

    def update(self, request, *args, **kwargs):
        reply_comment = get_object_or_404(CommentReply, pk=self.kwargs['reply_comment_pk'])
        if not request.user == reply_comment.replied_by:
            return Response("Not Allowed.Only owner can update reply.")
        return super().update(request, *args, **kwargs)





