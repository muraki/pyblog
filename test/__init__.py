# -*- coding: utf-8 -*-

from othello import *

# Test for Board class
class TestBoard:
    def __init__(self):
        self.board = Board()

    def testInstantiation(self):
        assert self.board

    def testGet(self):
        assert self.board.get(3, 3)

    def testInitialAssignment(self):
        assert self.board.get(3, 3) == BLACK
        
# 関数でテストを書く
def test_compare():
    assert 1==1
