from graphene_django import DjangoObjectType
import graphene
from home import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField


class UserType(DjangoObjectType):
    class Meta:
        model = User


class CategoryType(DjangoObjectType):
    class Meta:
        model = models.Category


class CategoryNode(DjangoObjectType):
    # pk = graphene.Int(source='pk')

    class Meta:
        model = models.Category
        interfaces = (relay.Node,)
        filter_fields = filter_fields = {
            'name': ['exact', 'icontains', 'istartswith']}


class TopicType(DjangoObjectType):
    class Meta:
        model = models.Topic


class PostType(DjangoObjectType):
    class Meta:
        model = models.Post


class CommentType(DjangoObjectType):
    class Meta:
        model = models.Comment


class Query(graphene.ObjectType):
    all_category = graphene.List(CategoryType)
    all_topic = graphene.List(TopicType)
    all_user = graphene.List(UserType)
    category_by_id = graphene.Field(CategoryType, id=graphene.Int(required=True))
    category_by_search = DjangoFilterConnectionField(CategoryNode)
    all_post = graphene.List(PostType)
    all_comment = graphene.List(CommentType)
    comments_by_id = graphene.Field(CommentType, id=graphene.Int(required=True))

    def resolve_all_category(root, info):
        return models.Category.objects.all()

    def resolve_all_topic(root, info):
        return models.Topic.objects.prefetch_related("category").all()

    def resolve_all_user(root, info):
        return User.objects.all()

    def resolve_category_by_id(root, info, id):
        # pk = kwargs.get('pk')
        return get_object_or_404(models.Category, id=id)

    def resolve_all_post(root, info):
        return models.Post.objects.all()

    def resolve_all_comments(root, info):
        return models.Comment.objects.prefetch_related('post').all()

    def resolve_comments_by_id(root, info, id):
        # pk = kwargs.get('pk')
        return get_object_or_404(models.Comment, id=id)


schema = graphene.Schema(query=Query)
