from django.urls import path,include
from home import views

urlpatterns=[
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.SignupView.as_view(), name='signup'),
    path('', views.CategoryList.as_view(), name='category_list'),
    path('<int:pk>/', views.TopicList.as_view(), name='category_topics'),
    path('<int:pk>/add/', views.new_topic, name='create_topic'),
    path('<int:pk>/topics/<int:topic_pk>/', views.PostListView.as_view(), name='topic_posts'),
    path('<int:pk>/topics/<int:topic_pk>/posts/add/', views.CreatePost.as_view(), name='add_post'),
    path('<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/comments', views.CommentListView.as_view(), name='comments'),
    path('<int:pk>/topics/<int:topic_pk>/reply/', views.reply_post, name='reply_topic'),
    path('<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/reply_post/', views.reply_post, name='reply_post'),
    path('<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/edit/', views.PostUpdateView.as_view(), name='edit_post'),
    path('<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/delete/', views.PostDeleteView.as_view(), name = 'delete_post'),
    path('<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/comments/<int:comment_pk>/edit', views.CommentUpdateView.as_view(), name='edit_comment'),
    path('<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/comments/<int:comment_pk>/delete', views.CommentDeleteView.as_view(), name='delete_comment'),
    path('<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/like/',views.PostLikeView.as_view(), name='post_like'),
    path('<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/comments/<int:comment_pk>/like/', views.CommentLikeView.as_view(), name='comment_like'),
    path('<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/like_detail/',views.PostLikeListView.as_view(), name= 'post_like_detail'),
    path('<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/comments/<int:comment_pk>/comment_detail/', views.CommentLikeListView.as_view(), name='comment_like_detail'),
    path('<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/comments/<int:comment_pk>/reply_comment', views.CommentReplyView.as_view(), name='comment_reply'),
    path('<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/comments/<int:comment_pk>/reply_comment/<int:reply_comment_pk>/update', views.CommentReplyUpdateView.as_view(), name='comment_reply_update'),
path('<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/comments/<int:comment_pk>/reply_comment/<int:reply_comment_pk>/delete', views.CommentReplyDeleteView.as_view(), name='comment_reply_delete'),
]