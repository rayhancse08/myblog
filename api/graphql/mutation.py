import graphene
from api.graphql.schema import CategoryType, TopicType
from home import models
from django.contrib.auth.models import User


class CategoryInput(graphene.InputObjectType):
    name = graphene.String()
    description = graphene.String()


class CreateCategory(graphene.Mutation):
    class Arguments:
        input = CategoryInput(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, input):
        category = models.Category()
        category.name = input.name
        category.description = input.description
        category.save()
        return CreateCategory(category=category)


class UpdateCategory(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=True)
        description = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name, id, description):
        category = models.Category.objects.get(id=id)
        category.name = name
        category.description = description
        category.save()
        return UpdateCategory(category=category)


class DeleteCategory(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    category = graphene.Field(CategoryType)

    def mutate(self, info, id):
        category = models.Category.objects.get(pk=id)
        if category is not None:
            category.delete()
        return DeleteCategory(category=category)


class CreateTopic(graphene.Mutation):
    class Arguments:
        subject = graphene.String()
        # last_updated = graphene.types.datetime.DateTime()
        category_id = graphene.Int()
        starter_id = graphene.Int()
        views = graphene.Int()

    topic = graphene.Field(TopicType)

    def mutate(self, info, subject, category_id, starter_id, views):
        topic = models.Topic()
        topic.subject = subject
        # topic.last_updated = last_updated
        category_obj = models.Category.objects.get(id=category_id)
        topic.category = category_obj
        starter_obj = User.objects.get(id=starter_id)
        topic.starter = starter_obj
        topic.views = views
        topic.save()
        return CreateTopic(topic=topic)


class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()
    create_topic = CreateTopic.Field()
