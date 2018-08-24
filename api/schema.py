import graphene
from graphene_django.types import DjangoObjectType
from django.db.models import Q

from .models import Board, Cell


# Queries
class BoardType(DjangoObjectType):
    flag_count = graphene.Int()

    class Meta:
        model = Board


class CellType(DjangoObjectType):
    class Meta:
        model = Cell


class Query(object):
    boards = graphene.List(BoardType)
    board = graphene.Field(BoardType, id=graphene.Int())

    cells = graphene.List(CellType, bomb=graphene.Boolean())
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

    def resolve_boards(self, info, **kwargs):
        return Board.objects.all()

    def resolve_cells(self, info, bomb=None, **kwargs):
        if bomb:
            filter = (
                Q(bomb__exact=bomb)
            )
            return Cell.objects.filter(filter)

        return Cell.objects.select_related('board').all()


# Mutations
class CreateBoard(graphene.Mutation):
    id = graphene.Int()
    height = graphene.Int()
    width = graphene.Int()
    bomb_count = graphene.Int()
    flag_count = graphene.Int()
    state = graphene.String()

    class Arguments:
        height = graphene.Int()
        width = graphene.Int()
        bomb_count = graphene.Int()

    def mutate(self, info, height, width, bomb_count):
        board = Board(height=height, width=width, bomb_count=bomb_count)
        board.save()

        return CreateBoard(
            id=board.id,
            height=board.height,
            width=board.width,
            bomb_count=board.bomb_count,
            flag_count=board.flag_count,
            state=board.state,
        )


class CreateCell(graphene.Mutation):
    board = graphene.Field(BoardType)
    x_loc = graphene.Int()
    y_loc = graphene.Int()
    bomb = graphene.Boolean()
    flagged = graphene.Boolean()
    discovered = graphene.Boolean()

    class Arguments:
        board_id = graphene.Int()
        x_loc = graphene.Int()
        y_loc = graphene.Int()
        bomb = graphene.Boolean()

    def mutate(self, info, board_id, x_loc, y_loc, bomb):
        board = Board.objects.filter(id=board_id).first()
        if not board:
            raise Exception('Invalid Board!')

        cell = Cell.objects.create(
            board=board,
            x_loc=x_loc,
            y_loc=y_loc,
            bomb=bomb,
        )

        return CreateCell(
            board=board,
            x_loc=cell.x_loc,
            y_loc=cell.y_loc,
            bomb=cell.bomb,
            flagged=cell.flagged,
            discovered=cell.discovered,
        )

class ClickCell(graphene.Mutation):
    cell = graphene.Field(lambda: CellType)

    class Arguments:
        id = graphene.Int()

    def mutate(self, info, id):
        cell = Cell.objects.get(pk=id)
        if not cell:
            raise Exception('Invalid Cell!')

        cell.click()

        return ClickCell(
            cell=cell
        )

class FlagCell(graphene.Mutation):
    cell = graphene.Field(lambda: CellType)

    class Arguments:
        id = graphene.Int()

    def mutate(self, info, id):
        cell = Cell.objects.get(pk=id)
        if not cell:
            raise Exception('Invalid Cell!')

        cell.toggle_flag()

        return FlagCell(
            cell=cell
        )


class Mutation(graphene.ObjectType):
    create_board = CreateBoard.Field()
    create_cell = CreateCell.Field()
    click_cell = ClickCell.Field()
    flag_cell = FlagCell.Field()
