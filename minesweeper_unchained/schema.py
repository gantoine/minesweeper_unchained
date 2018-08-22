import graphene

import sweeper.schema
import sweeper.schema_relay


class Query(
  sweeper.schema.Query,
  sweeper.schema_relay.RelayQuery,
  graphene.ObjectType
):
    pass

class Mutation(
  sweeper.schema.Mutation,
  sweeper.schema_relay.RelayMutation,
  graphene.ObjectType
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
