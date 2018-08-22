import graphene
from graphene_django.types import DjangoObjectType

from .models import Board, Cell


class BoardType(DjangoObjectType):
    class Meta:
        model = Board


class CellType(DjangoObjectType):
    class Meta:
        model = Cell


class Query(object):
    all_boards = graphene.List(BoardType)
    board = graphene.Field(BoardType, id=graphene.Int())

    all_cells = graphene.List(CellType)
    cell = graphene.Field(CellType,
                        id=graphene.Int(),
                        x_loc=graphene.Int(),
                        y_loc=graphene.Int(),)

    def resolve_board(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Board.objects.get(pk=id)

        return None

    def resolve_cell(self, info, **kwargs):
        id = kwargs.get('id')
        x_loc = kwargs.get('x_loc')
        y_loc = kwargs.get('y_loc')

        if id is not None:
            return Cell.objects.get(pk=id)

        if x_loc is not None and y_loc is not None:
            return Cell.objects.get(x_loc=x_loc, y_loc=y_loc)

        return None

    def resolve_all_boards(self, info, **kwargs):
        return Board.objects.all()

    def resolve_all_cells(self, info, **kwargs):
        return Cell.objects.select_related('board').all()
