import graphene

import api.schema
# import api.schema_relay


class Query(
  api.schema.Query,
  # api.schema_relay.RelayQuery,
  graphene.ObjectType
):
    pass

class Mutation(
  api.schema.Mutation,
  # api.schema_relay.RelayMutation,
  graphene.ObjectType
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
