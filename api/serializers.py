from rest_framework import serializers

from .models import Board, Cell

class BoardSerializer(serializers.Serializer):
    class Meta:
        model = Board
        fields = ('id', 'height', 'width', 'bomb_count', 'state')

class CellSerializer(serializers.Serializer):
    class Meta:
        model = Cell
        fields = ('id', 'x_loc', 'y_loc', 'bomb', 'flagged', 'discovered', 'mine_count')
