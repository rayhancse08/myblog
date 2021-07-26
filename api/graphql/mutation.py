import graphene
from api.graphql.schema import CategoryType
from home import models


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


class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()
