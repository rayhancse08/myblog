from django.shortcuts import render, reverse, redirect
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView
from .models import Category, Topic, Post, Comment, PostLike, CommentLike, CommentReply
from .forms import CategoryForm, TopicForm, PostForm, CommentForm, SignupForm, CommentReplyForm
from django.shortcuts import HttpResponse, get_object_or_404, get_list_or_404
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.template.loader import render_to_string


# Create your views here.


class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = 'registration/signup_form.html'
    success_url = reverse_lazy('category_list')


@method_decorator([login_required], name='dispatch')
class CreatePost(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'home/create_post.html'

    def form_valid(self, form):
        topic = get_object_or_404(Topic, pk=self.kwargs['topic_pk'])
        post = form.save(commit=False)
        post.created_by = self.request.user
        post.topic = topic
        post.save()
        return redirect('topic_posts', pk=post.topic.category.pk, topic_pk=post.topic.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['topic_pk'] = self.kwargs['topic_pk']
        return context


class CategoryList(ListView):
    model = Category
    template_name = 'home/category_list.html'
    context_object_name = 'categories'
    paginate_by = 10


class TopicList(ListView):
    model = Topic
    template_name = 'home/topics.html'
    context_object_name = 'topics'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        queryset = self.category.topics.order_by('-last_updated').annotate(
            replies=Count('posts'))                      # Retrieve topics for requested category and count topic wise post
        return queryset


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'home/topics_posts.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session_key = self.topic.pk
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True
        context['topic'] = self.topic
        context['session_key'] = session_key
        context['request_user'] = self.request.user
        return context

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, category__pk=self.kwargs.get('pk'),
                                       pk=self.kwargs.get('topic_pk'))  # filtering with category id and topic id
        queryset = self.topic.posts.order_by('created_at')  # Retrieve post
        return queryset


@login_required
def new_topic(request, pk):

    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.category = category
            topic.starter = request.user
            topic.save()  # add topic
            Post.objects.create(
                title=form.cleaned_data['title'],
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )

            messages.success(request, 'Topic is created')
            return redirect('category_topics', pk=pk)

    else:
        form = TopicForm()

    return render(request, 'home/create_topic.html', {'category': category, 'form': form})


@login_required
def reply_post(request, pk, topic_pk, post_pk):

    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.created_user = request.user
            comment.save()
            return redirect('comments', pk=pk, topic_pk=topic_pk, post_pk=post_pk)
    else:
        form = CommentForm()

    return render(request, 'home/reply_topic.html', {'form': form, 'post': post})


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('title', 'message',)
    template_name = 'home/edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('comments', pk=post.topic.category.pk, topic_pk=post.topic.pk, post_pk=post.pk)


@method_decorator(login_required, name='dispatch')
class PostDeleteView(DeleteView):
    model = Post
    context_object_name = 'post'
    pk_url_kwarg = 'post_pk'

    def get_success_url(self):
        return reverse_lazy('topic_posts', kwargs={'pk': self.kwargs['pk'], 'topic_pk': self.kwargs['topic_pk']})


class CommentListView(ListView):
    model = Post
    context_object_name = 'comments'
    template_name = 'home/post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topic'] = get_object_or_404(Topic, category__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        context['post'] = context['topic'].posts.get(pk=self.kwargs.get('post_pk'))
        context['request_user'] = self.request.user
        return context

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_pk'), topic__pk=self.kwargs.get('topic_pk'))
        queryset = post.comments.order_by('created_time')
        return queryset


@method_decorator(login_required, name='dispatch')
class CommentUpdateView(UpdateView):
    model = Comment
    fields = ('message',)
    template_name = 'home/edit_comment.html'
    pk_url_kwarg = 'comment_pk'
    context_object_name = 'comment'

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.updated_user = self.request.user
        comment.updated_time = timezone.now()
        comment.save()
        return redirect('comments', pk=comment.post.topic.category.pk, topic_pk=comment.post.topic.pk,
                        post_pk=comment.post.pk)


@method_decorator(login_required, name='dispatch')
class CommentDeleteView(DeleteView):
    model = Comment
    context_object_name = 'comment'
    pk_url_kwarg = 'comment_pk'

    def get_success_url(self):
        return reverse_lazy('comments', kwargs={'pk': self.kwargs['pk'], 'topic_pk': self.kwargs['topic_pk'],
                                                'post_pk': self.kwargs['post_pk']})


@method_decorator(login_required, name='dispatch')
class PostLikeView(CreateView):
    model = PostLike
    template_name = 'home/like.html'

    def get(self, request, *args, **kwargs):
        request_user = self.request.user
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        already_liked = PostLike.objects.filter(post=post.id, liked_by=request_user)
        if already_liked:
            already_liked.delete()

        else:
            PostLike.objects.create(post=post, liked_by=request_user)
        return redirect('comments', pk=post.topic.category.pk, topic_pk=post.topic.pk, post_pk=post.pk)


@method_decorator(login_required, name='dispatch')
class CommentLikeView(CreateView):
    model = CommentLike
    template_name = 'home/like.html'

    def get(self, request, *args, **kwargs):

        request_user = self.request.user
        comment = get_object_or_404(Comment, pk=self.kwargs['comment_pk'])
        already_liked = CommentLike.objects.filter(comment=comment.id, comment_liked_by=request_user)
        if already_liked:
            already_liked.delete()

        else:
            CommentLike.objects.create(comment=comment, comment_liked_by=request_user)
        return redirect('comments', pk=comment.post.topic.category.pk, topic_pk=comment.post.topic.pk,
                        post_pk=comment.post.pk)


class PostLikeListView(ListView):
    model = PostLike
    context_object_name = 'post_likes'
    template_name = 'home/like.html'

    def get_queryset(self):
        queryset = get_list_or_404(PostLike, post=self.kwargs['post_pk'])
        return queryset

    def get(self, request, *args, **kwargs):
        like = get_list_or_404(PostLike, post=self.kwargs['post_pk'])
        data = dict()

        data['like'] = render_to_string('home/like.html', {'post_likes': like}, request=request)
        return JsonResponse(data)


class CommentLikeListView(ListView):
    model = CommentLike
    context_object_name = 'comment_likes'
    template_name = 'home/like.html'

    def get_queryset(self):
        queryset = get_list_or_404(CommentLike, comment=self.kwargs['comment_pk'])
        return queryset

    def get(self, request, *args, **kwargs):
        comment = get_list_or_404(CommentLike, comment=self.kwargs['comment_pk'])
        data = dict()

        data['like'] = render_to_string('home/like.html', {'comment_likes': comment}, request=request)
        return JsonResponse(data)

@method_decorator(login_required,name='dispatch')
class CommentReplyView(CreateView):
    model = CommentReply
    form_class = CommentReplyForm
    template_name = 'home/reply_comment.html'

    def form_valid(self, form):
        comment = get_object_or_404(Comment, pk=self.kwargs['comment_pk'])
        comment_reply = form.save(commit=False)
        comment_reply.comment = comment
        comment_reply.replied_by = self.request.user
        comment_reply.save()
        return redirect('comments', pk=comment.post.topic.category.pk, topic_pk=comment.post.topic.pk, post_pk=comment.post.pk)

@method_decorator(login_required,name='dispatch')
class CommentReplyUpdateView(UpdateView):
    model = CommentReply
    form_class = CommentReplyForm
    pk_url_kwarg = 'reply_comment_pk'
    context_object_name = 'reply_comment'
    template_name = 'home/comment_reply_update_form.html'

    def get_success_url(self):
        return reverse_lazy('comments',
                            kwargs={'pk':self.kwargs['pk'], 'topic_pk':self.kwargs['topic_pk'],'post_pk':self.kwargs['post_pk']})



@method_decorator(login_required,name='dispatch')
class CommentReplyDeleteView(DeleteView):
    model = CommentReply
    context_object_name = 'reply_comment'
    template_name = 'home/reply_comment_confirm_delete.html'
    pk_url_kwarg = 'reply_comment_pk'

    def get_success_url(self):
        return reverse_lazy('comments',
                            kwargs={'pk':self.kwargs['pk'],'topic_pk':self.kwargs['topic_pk'],'post_pk':self.kwargs['post_pk']})
