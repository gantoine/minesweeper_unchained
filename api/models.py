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

    def  __str__(self):
      return "%sx%s %sB %s" % (self.height, self.width, self.bomb_count, self.state)

    def populate(self):
      if self.cell_set.all().exists():
        return

      bombs = [True] * self.bomb_count + [False] * (self.width * self.height - self.bomb_count)
      random.shuffle(bombs)
      proto_board = mat(bombs).reshape(self.width, self.height)

      for i in range(self.width):
        for j in range(self.height):
          Cell.objects.create(
            board=self,
            x_loc=i,
            y_loc=j,
            bomb=proto_board[i, j],
          )

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
