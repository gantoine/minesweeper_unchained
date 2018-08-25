import graphene
from graphene_django_subscriptions.subscription import Subscription
from .serializers import BoardSerializer, CellSerializer


class BoardSubscription(Subscription):
    class Meta:
        serializer_class = BoardSerializer
        stream = 'boards'
        description = 'Board Subscription'


class CellSubscription(Subscription):
    class Meta:
        serializer_class = CellSerializer
        stream = 'cells'
        description = 'Cell Subscription'
