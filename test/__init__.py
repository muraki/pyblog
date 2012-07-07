# -*- coding: utf-8 -*-

from othello import *

# Test for Board class
class TestBoard:
    def __init__(self):
        self.board = Board()

    def test_instantiation(self):
        assert self.board

    def test_get(self):
        assert self.board.get(3, 3)

    def test_initial_assignment(self):
        assert self.board.get(3, 3) == BLACK
        

def test_find_turnable_points():
    board = Board()
    print find_turnable_points(board, BLACK)

test_find_turnable_points()
