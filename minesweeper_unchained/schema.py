import graphene

import sweeper.schema


class Query(sweeper.schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
