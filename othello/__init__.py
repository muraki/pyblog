# -*- coding: utf-8 -*-

from itertools import izip
import random

EMPTY = 0
BLACK = 1
WHITE = 2

class Board(object):
    rows = []
    def __init__(self):
        for i in xrange(8):
            row = [0] * 8
            self.rows.append(row)
        self.put(3, 3, BLACK)
        self.put(4, 3, WHITE)
        self.put(3, 4, WHITE)
        self.put(4, 4, BLACK)

    def put(self, row, col, piece):
        self.rows[row][col] = piece

    def get(self, row, col):
        return self.rows[row][col]

    @classmethod
    def _turned(cls, pieces):
        a = list(pieces)
        me = a.pop(0)
        if a[0] != me and me in a:
            idx = a.index(me)
            a = [me] * idx + a[idx:]
        return [me] + a

    def eight_pieces_until_empty(self, row, col):
        for points in self.around8_points(row, col):
            pieces = []
            for i, j in points:
                piece = self.get(i, j) 
                if piece == EMPTY:
                    break
                else:
                    pieces.append(piece)
            yield pieces

    def has_any_turnable_pieces(self, row, col, cur_p):
        rev_p = piece_rev(cur_p)
        pieces8 = list(self.eight_pieces_until_empty(row, col))
        filtered_pieces8 = [pieces for pieces in pieces8 if len(pieces) >= 3] # 調べる必要のないものは捨てている
        if not filtered_pieces8:
            return False
        for pieces in filtered_pieces8:
            if pieces != self._turned(pieces):
                return True
        return False

    def update(self, row, col, cur_p):
        rev_p = piece_rev(cur_p)
        #print list(self.around8_points(row, col))
        #print list(self.eight_pieces_until_empty(row, col))
        for points, pieces in izip(self.around8_points(row, col), self.eight_pieces_until_empty(row, col)):
            if len(pieces) < 3:
                continue
            if pieces == self._turned(pieces):
                continue
            points.pop(0)
            for i, j in points:
                p = self.get(i, j)
                if p == rev_p:
                    self.put(i, j, cur_p)
                else:
                    assert p == cur_p
                    break

    @classmethod
    def around8_points(self, row, col):
        def inc(n):
            return range(n, 8)
        def dec(n):
            return range(n, -1, -1)
        def cons(n):
            return [n] * 8
        operators = (inc, dec, cons)
        op_conbination = [(op1, op2) for op1 in operators for op2 in operators if (op1, op2) != (cons, cons)]
        for f, g in op_conbination:
            yield zip(f(row), g(col))

    def display(self):
        print ' |%s|' % ('|'.join([str(i) for i in range(1, 8 + 1)]))
        for j, row in enumerate(self.rows):
            print '%d|%s|'% (j + 1, '|'.join([piece_conv(p) for p in row]))

def piece_rev(p):
    if p == WHITE:
        return BLACK
    elif p == BLACK:
        return WHITE
    else:
        assert False

def piece_conv(p):
    if p == EMPTY:
        return u' '
    elif p == WHITE:
        return u'○'
    elif p == BLACK:
        return u'●'
    else:
        assert False

class HumanInputError(Exception):
    pass

class GameOver(Exception):
    COMPLETE = 1
    CANNOT_PUT = 2
    def __init__(self, status, looser=None):
        self.status = status
        self.looser = looser

def human_input(board, piece):
    try:
        col = raw_input('yoko?')
        col = int(col) - 1
        row = raw_input('tate?')
        row = int(row) - 1
    except ValueError, e:
        raise HumanInputError(u'1-8の数字を入力して下さい')
    if board.get(row, col) != EMPTY:
        raise HumanInputError(u'そこにはおけません')
    board.put(row, col, piece)
    if not board.has_any_turnable_pieces(row, col, piece):
        board.put(row, col, EMPTY) # 元に戻す
        raise HumanInputError(u'そこにはおけません')
    return row, col

def iter_points():
    for i in range(8):
        for j in range(8):
            yield i, j

def find_turnable_points(board, cur_p):
    for row, col in iter_points():
        if board.get(row, col) != EMPTY:
            continue
        board.put(row, col, cur_p)
        ok = board.has_any_turnable_pieces(row, col, cur_p)
        board.put(row, col, EMPTY) # 元に戻す
        if ok:
            yield row, col

def main_loop(board):
    for player, piece in [('human', BLACK), ('computer', WHITE)]:
        if not [None for row, col in iter_points() if board.get(row, col) == EMPTY]:
            raise GameOver(GameOver.COMPLETE)
        if player == 'human':
            if not list(find_turnable_points(board, piece)):
                raise GameOver(GameOver.CANNOT_PUT, looser=player)
            while True:
                board.display()
                print '%s, your turn[%s]:' % (player, piece_conv(piece))
                try:
                    row, col = human_input(board, piece)
                except HumanInputError, e:
                    print unicode(e)
                else:
                    break
            board.update(row, col, piece)
        else:
            if not list(find_turnable_points(board, piece)):
                raise GameOver(GameOver.CANNOT_PUT, looser=player)
            print '%s, your turn[%s]:' % (player, piece_conv(piece))
            points = list(find_turnable_points(board, piece))
            row, col = random.choice(points)
            print 'computer put (%d, %d).' % (col + 1, row + 1)
            board.put(row, col, piece)
            board.update(row, col, piece)

def main():
    board = Board()
    try:
        while True:
            main_loop(board)
    except GameOver, go:
        if go.status == GameOver.CANNOT_PUT:
            if go.looser == 'human':
                print u'＼(^o^)／'
            else:
                print 'you win!'
        elif go.status == GameOver.COMPLETE:
            human = 0
            for row, col in iter_points():
                if board.get(row, col) == BLACK:
                    human += 1
            all_count = 8 * 8
            print 'Result human:%d computer:%d' % (human, all_count - human)
            if human > all_count // 2:
                print 'you win!'
            elif human == half // 2:
                print 'draw...'
            else:
                print u'＼(^o^)／'
        else:
            assert False

if __name__ == '__main__':
    main()
