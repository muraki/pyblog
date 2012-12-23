# -*- coding: utf-8 -*-
import os

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return u'超こんにちは、世界abc'


from othello import Board, main_loop, GameOver
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
