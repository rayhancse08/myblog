import graphene
from api.graphql.schema import Query
from api.graphql.mutation import Mutation

schema = graphene.Schema(query=Query, mutation=Mutation)
