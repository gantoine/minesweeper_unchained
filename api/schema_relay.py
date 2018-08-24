# Experiments with Relay

import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay.node.node import from_global_id

from .models import Board, Cell


# Queries
class BoardFilter(django_filters.FilterSet):
    class Meta:
        model = Board
        fields = ['state']


class BoardNode(DjangoObjectType):
    class Meta:
        model = Board
        interfaces = (graphene.relay.Node, )


class CellFilter(django_filters.FilterSet):
    class Meta:
        model = Cell
        fields = ['bomb', 'flagged', 'discovered']


class CellNode(DjangoObjectType):
    class Meta:
        model = Cell
        interfaces = (graphene.relay.Node,)


class RelayQuery(graphene.ObjectType):
    relay_board = graphene.relay.Node.Field(BoardNode)
    relay_boards = DjangoFilterConnectionField(BoardNode, filterset_class=BoardFilter)

    relay_cell = graphene.relay.Node.Field(CellNode)
    relay_cells = DjangoFilterConnectionField(CellNode, filterset_class=CellFilter)


# Mutations
class RelayCreateBoard(graphene.relay.ClientIDMutation):
    board = graphene.Field(BoardNode)

    class Input:
        height = graphene.Int()
        width = graphene.Int()
        bomb_count = graphene.Int()

    def mutate_and_get_payload(root, info, **input):
        board = Board(
            height=input.get('height'),
            width=input.get('width'),
            bomb_count=input.get('bomb_count'),
        )
        board.save()

        return RelayCreateBoard(board=board)


class RelayCreateCell(graphene.relay.ClientIDMutation):
    cell = graphene.Field(CellNode)

    class Input:
        board_id = graphene.Int()
        x_loc = graphene.Int()
        y_loc = graphene.Int()
        bomb = graphene.Boolean()

    def mutate_and_get_payload(root, info, **input):
        cell = Cell(
            board = Board.objects.find(pk=board_id),
            x_loc = input.get('x_loc'),
            y_loc = input.get('y_loc'),
            bomb = input.get('bomb'),
        )
        cell.save()

        return RelayCreateCell(cell=cell)

class RelayClickCell(graphene.relay.ClientIDMutation):
    discovered = graphene.Boolean()

    class Arguments:
        id = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        id = from_global_id(input.get('id'))
        cell = Cell.objects.get(pk=id)

        if not cell:
            raise Exception('Invalid Cell!')

        cell.click()

        return RelayClickCell(
            discovered=cell.discovered,
        )

class RelayFlagCell(graphene.relay.ClientIDMutation):
    flagged = graphene.Boolean()

    class Arguments:
        id = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        id = from_global_id(input.get('id'))
        cell = Cell.objects.get(pk=id)

        if not cell:
            raise Exception('Invalid Cell!')

        cell.flag()

        return RelayClickCell(
            flagged=cell.flagged,
        )


class RelayMutation(graphene.AbstractType):
    relay_create_board = RelayCreateBoard.Field()
    relay_create_cell = RelayCreateCell.Field()
    relay_click_cell = RelayClickCell.Field()
    relay_flag_cell = RelayFlagCell.Field()
