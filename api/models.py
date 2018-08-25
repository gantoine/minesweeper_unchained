# The three-step guide to making model changes:
#
# Change your models (in models.py).
# Run python manage.py makemigrations to create migrations for those changes
# Run python manage.py migrate to apply those changes to the database.

import os
import dj_database_url
import psycopg2

from django.db import models
from django.utils import timezone
from numpy import random, mat, array

# Create your models here.
class Board(models.Model):
    height = models.IntegerField(default=10)
    width = models.IntegerField(default=10)
    bomb_count = models.IntegerField(default=10)
    # active, solved, failed
    state = models.CharField(max_length=200, default='active')
    last_move = models.DateTimeField('last move', default=timezone.now)

    @property
    def flag_count(self):
      return self.cell_set.filter(flagged=True).count()

    def  __str__(self):
      return "%sx%s %sB %s" % (self.height, self.width, self.bomb_count, self.state)

    def reset(self):
      self.state = 'active'
      self.save()

      self.cell_set.all().delete()
      self.populate()

    def fail(self):
      self.state = 'failed'
      self.save()

      self.cell_set.filter(discovered=False, bomb=True).update(discovered=True)
      self.cell_set.filter(discovered=False, flagged=True).update(discovered=True)

    def solve(self):
      self.state = 'solved'
      self.save()

    def cell_clicked(self, cell):
      if cell.bomb:
        self.fail()

    def cell_flagged(self):
      if self.cell_set.filter(flagged=True, bomb=True).count() == self.bomb_count:
        self.solve()

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

      sql = """INSERT INTO api_cell(board_id, x_loc, y_loc, bomb, flagged, discovered, mine_count)
             VALUES"""

      for i in range(self.width):
        for j in range(self.height):
          mine_count = build_mine_count_for_cell(proto_board, i, j, self.width, self.height)
          sql = sql + "(%s, %s, %s, %s, %s, %s, %s)," % (self.id, i, j, proto_board[i, j], False, False, mine_count)

      conn = setup_connection()
      conn.cursor().execute(sql[:-1])
      conn.commit()
      teardown_connection(conn)

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

    def click(self):
      self.discover()
      self.board.cell_clicked(self)

      if self.board.state == 'failed':
        return;

      if self.mine_count == 0:
        cell_ids = []
        self.clear_neighbors(self.board.cell_set, cell_ids)
        Cell.objects.filter(pk__in=cell_ids).update(discovered=True)

    def discover(self):
      self.discovered = True
      self.save()

    def clear_neighbors(self, cells, cell_ids):
      for i in [0, 1, -1]:
        for j in [0, 1, -1]:
          try:
            if i == 0 and j == 0:
              continue

            cell = cells.get(
              x_loc=self.x_loc + i,
              y_loc=self.y_loc + j,
              discovered=False,
              flagged=False,
              bomb=False,
            )

            if cell.id in cell_ids:
              continue

            cell_ids.append(cell.id)

            if cell.mine_count == 0:
              cell.clear_neighbors(cells, cell_ids)

          except Cell.DoesNotExist:
            pass

    def toggle_flag(self):
      if self.discovered:
        return

      new_flag = not self.flagged
      if (new_flag and self.board.can_flag()) or (not new_flag and self.board.can_unflag()):
        self.flagged = new_flag
        self.save()

        self.board.cell_flagged()

# Helper methods
def setup_connection():
  db_config = dj_database_url.config()
  conn = psycopg2.connect(
    database = db_config['NAME'],
    user = db_config['USER'],
    password = db_config['PASSWORD'],
    host = db_config['HOST']
  )
  return conn

def teardown_connection(conn):
  conn.cursor().close()
  conn.close()

def build_mine_count_for_cell(proto_board, x, y, width, height):
  mine_count = 0

  for k in [0, 1, -1]:
    for l in [0, 1, -1]:
      if (x + k == width) or (x + k < 0) or (y + l == height) or (y + l < 0):
        continue

      if x == 0 and y == 0:
        continue

      bomb = proto_board[x + k, y + l]
      if bomb:
        mine_count += 1

  return mine_count
