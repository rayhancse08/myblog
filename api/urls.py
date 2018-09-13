from django.urls import path,include
from api import views
from rest_framework.routers import DefaultRouter


router=DefaultRouter()
router.register(prefix='category',viewset=views.CategoryAPIViewSet,base_name='category_api')
router.register(prefix='category/(?P<pk>[^/.]+)/topic',viewset=views.TopicAPIViewSet,base_name='topic_api')
router.register(prefix='category/(?P<pk>[^/.]+)/topic/(?P<topic_pk>[^/.]+)/posts',viewset=views.PostAPIViewSet,base_name='post_api')
router.register(prefix='category/(?P<pk>[^/.]+)/topic/(?P<topic_pk>[^/.]+)/posts/(?P<post_pk>[^/.]+)/comments',viewset=views.CommentAPIViewSet,base_name='comment_api')
router.register(prefix='category/(?P<pk>[^/.]+)/topic/(?P<topic_pk>[^/.]+)/posts/(?P<post_pk>[^/.]+)/comments/(?P<comment_pk>[^/.]+)/replies',viewset=views.ReplyCommentAPIViewSet,base_name='reply_comment_api')

urlpatterns=[
    path('api_auth/',include('rest_framework.urls')),
    path('category/<int:pk>/create_topic/',views.CreateTopicAPIView.as_view(),name='topic_create_api'),
    path('',include(router.urls),name='api_router'),
    path('category/<int:pk>/topic/<int:topic_pk>/posts/<int:post_pk>/likes/',views.PostLikeAPIView.as_view(),name='post_likes'),
    path('category/<int:pk>/topic/<int:topic_pk>/posts/<int:post_pk>/comments/<int:comment_pk>/likes/',views.CommentLikeAPIView.as_view(),name='comment_likes')



]
