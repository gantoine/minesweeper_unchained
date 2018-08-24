# The three-step guide to making model changes:
#
# Change your models (in models.py).
# Run python manage.py makemigrations to create migrations for those changes
# Run python manage.py migrate to apply those changes to the database.

from django.db import models
from django.utils import timezone
from numpy import random, mat

# Create your models here.
class Board(models.Model):
    height = models.IntegerField(default=10)
    width = models.IntegerField(default=10)
    bomb_count = models.IntegerField(default=10)
    # ready, playing, solved, failed
    state = models.CharField(max_length=200, default='ready')
    last_move = models.DateTimeField('last move', default=timezone.now)

    @property
    def flag_count(self):
      return self.cell_set.filter(flagged=True).count()

    def  __str__(self):
      return "%sx%s %sB %s" % (self.height, self.width, self.bomb_count, self.state)

    def reset(self):
      self.state = 'ready'
      self.save()

    def fail(self):
      self.state = 'failed'
      self.save()

    def cell_clicked(self, cell):
      if cell.bomb:
        self.fail()

    def can_flag(self):
      return self.bomb_count > self.flag_count

    def can_unflag(self):
      return self.flag_count > 0

    def populate(self):
      if self.cell_set.all().exists():
        return

      bombs = [True] * self.bomb_count + [False] * (self.width * self.height - self.bomb_count)
      random.shuffle(bombs)
      proto_board = mat(bombs).reshape(self.width, self.height)

      for i in range(self.width):
        for j in range(self.height):
          cell = Cell.objects.create(
            board=self,
            x_loc=i,
            y_loc=j,
            bomb=proto_board[i, j],
          )
          cell.set_mine_count(proto_board)

class Cell(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    x_loc = models.IntegerField(default=0)
    y_loc = models.IntegerField(default=0)
    bomb = models.BooleanField(default=False)
    flagged = models.BooleanField(default=False)
    discovered = models.BooleanField(default=False)
    mine_count = models.IntegerField(default=0)

    def  __str__(self):
      bomb = 'B' if self.bomb else ''
      flagged = 'F' if self.flagged else ''
      discovered = 'D' if self.discovered else ''
      return "%s,%s %s %s %s" % (self.x_loc, self.y_loc, bomb, flagged, discovered)

    def set_mine_count(self, proto_board):
      if self.x_loc - 1 > 0:
        if proto_board[self.x_loc - 1, self.y_loc]:
          self.mine_count += 1

      if self.y_loc - 1 > 0:
        if proto_board[self.x_loc, self.y_loc - 1]:
          self.mine_count += 1

      if self.x_loc + 1 < self.board.width:
        if proto_board[self.x_loc + 1, self.y_loc]:
          self.mine_count += 1

      if self.y_loc + 1 < self.board.height:
        if proto_board[self.x_loc, self.y_loc + 1]:
          self.mine_count += 1

      self.save()

    def click(self):
      self.discovered =True
      self.save()

      self.board.cell_clicked(self)

    def toggle_flag(self):
      if self.discovered:
        return

      new_flag = not self.flagged
      if (new_flag and self.board.can_flag()) or (not new_flag and self.board.can_unflag()):
        self.flagged = new_flag
        self.save()
