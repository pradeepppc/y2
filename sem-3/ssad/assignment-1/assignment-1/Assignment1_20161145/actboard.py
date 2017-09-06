from Enemy import *
from Bomberman import *
from Bomb import *
import numpy as np
import os
from brick import *

from getchunix import *
from alarmexception import *
import random

getch = GetchUnix()
class Board():

    x_border = 76
    y_border = 44
    board = []
    def __init__(self, x, y):
        self.x_border = x
        self.y_border = y

    def printBoard(self):
        l1 = []
        l2 = []
        l3 = []
        for i in range(self.x_border):
            l1.append('X')
        i = 0
        for i in range(self.x_border):
            if 0 <= i <= 3 or self.x_border - 4 <= i <= self.x_border - 1:
                l2.append('X')
            else:
                l2.append(' ')
        k = 0
        i = 0
        for i in range(self.x_border):
            if 0 <= k <= 3:
                l3.append('X')
                k += 1
                continue
            elif 4 <= k <= 7:
                l3.append(' ')
                k += 1
                if k == 8:
                    k = 0
        h = 0
        i = 0
        for i in range(self.y_border):
            if (i >= 0 and i <= 1) or (i == self.y_border - 2
                                       or i == self.y_border - 1):
                self.board.append(l1)
                continue
            else:
                if h == 0 or h == 1:
                    self.board.append(l2)
                    h += 1
                    continue
                else:
                    self.board.append(l3)
                    h += 1
                    if h > 3:
                        h = 0
                        continue
        i = 0

        board_array = np.array(self.board)
        return board_array


    def printb(self):
        board_arr = self.printBoard()
        for i in range(4):
            board_arr[2][i+4] = 'B'
            board_arr[3][i+4] = 'B'
            board_arr[4][i+44] = 'E'
            board_arr[5][i+44] = 'E'
            board_arr[26][i+44] = 'E'
            board_arr[27][i+44] = 'E'
            board_arr[16][i+28] = 'E'
            board_arr[17][i+28] = 'E'
            board_arr[28+8][i+36] = 'E'
            board_arr[29+8][i+36] = 'E'
            board_arr[32+8-2][i+36] = '/'
            board_arr[33+8-2][i+36] = '/'
            board_arr[16][i+36] = '/'
            board_arr[17][i+36] = '/'
        for i in range(self.y_border):
            x = ''
            for k in range(self.x_border):
                x += str(board_arr[i][k])
            print(x)

    def update_board(self, lisp, n, flag, br):
                board_arr = self.printBoard()
                for j in range(4):
                    for k in range(n):
                        board_arr[lisp[k][1] - 1][lisp[k][0] - 1 + j] = 'E'
                        board_arr[lisp[k][1]][lisp[k][0] - 1 + j] = 'E'
                    for k in range(br):
                        board_arr[lisp[k+n][1] - 1][lisp[k+n][0] - 1 + j] = '/'
                        board_arr[lisp[k+n][1]][lisp[k+n][0] - 1 + j] = '/'

                    board_arr[lisp[n+br][1]-1][lisp[n+br][0]-1+j] = 'B'
                    board_arr[lisp[n+br][1]][lisp[n+br][0]+j-1] = 'B'
                    if (len(lisp) == n + 2 + br):
                        if flag == 0:
                            board_arr[lisp[n+br+1][1] - 1][lisp[n+br+1][0] - 1 + j] = 'O'
                            board_arr[lisp[n+br+1][1]][lisp[n+br+1][0] + j - 1] = 'O'
                        else:
                            board_arr[lisp[n+br + 1][1] - 1][lisp[n+br + 1][0] - 1 + j] = 'e'
                            board_arr[lisp[n+br + 1][1]][lisp[n+br + 1][0] + j - 1] = 'e'


                for i in range(self.y_border):
                    x = ''
                    for k in range(self.x_border):
                        x += str(board_arr[i][k])
                    print(x)



bomberman = Bomberman()
gameexit = False

def alarmHandler(signum, frame):
    raise AlarmException
def input_to(timeout=1):
    signal.signal(signal.SIGALRM, alarmHandler)
    signal.alarm(timeout)
    try:
        text = getch()
        signal.alarm(0)
        return text
    except AlarmException:
        print("\n Prompt timeout. Continuing...")
    signal.signal(signal.SIGALRM, signal.SIG_IGN)
    return ''

def check_pos(l1, l2, l3, l4, l5, l6, l7, l8):
    if l2[l1[1]-1][l1[0] - 1] == 'X':
        return False
    left = [l3, l4, l5, l6, l7, l8]
    for i in range(6):
        if ((l1[0] == left[i][0]) and (l1[1] == left[i][1])):
            return False
    return True


def startgame():
    boa = Board(76, 44)      #creating board
#creating bomberman
    e1 = Enemy()
    e2 = Enemy()
    e3 = Enemy()
    e4 = Enemy()
    b1 = Brick()
    b2 = Brick()
    b1.set_cord(37, 39)
    b2.set_cord(29 + 8, 17)
    e1.set_position(45, 5)
    e2.set_position(45, 27)
    e3.set_position(29, 17)
    e4.set_position(37, 29 + 8)
    bomberman.set_position(5, 3)#initial position of bomberman

    boa.printb()
    #os.system('clear')
    lop = 0
    bombframes = 0
    bomb_pos = []
    n = 4
    br = 2
    while True:
        print('Number of lives remaining are :' + ' ' +
              str(bomberman.get_life()) + '                      ' + 'SCORE : ' +
              str(bomberman.get_score()))

        flag = 0
        #os.system('clear')
        #c = str(raw_input('enter'))
        c = input_to()
        tup_pos = bomberman.get_position()

        board_now = boa.printBoard()
        lisp = []
        enlisp = [[4, 0], [-4, 0], [0, 2], [0, -2]]

        lp = enlisp[random.randrange(4)]
        lp1 = np.array(lp)
        if(e1.get_life() == 1):

            e1ar = e1.get_position()
            lp1[0] = lp1[0] + e1ar[0]
            lp1[1] = lp[1] + e1ar[1]
            if(check_pos(lp1, board_now, e1.get_position(), e2.get_position(),
                         e3.get_position(), e4.get_position(), b1.ret_cord(), b2.ret_cord())):
                e1.set_position(lp1[0], lp1[1])
            lisp.append(e1.get_position())
            lpa = enlisp[random.randrange(4)]
            lp1[0] = lpa[0]
            lp1[1] = lpa[1]
        if(e2.get_life() == 1):
            e2ar = e2.get_position()
            lp1[0] = lp1[0] + e2ar[0]
            lp1[1] = lp[1] + e2ar[1]
            if (check_pos(lp1, board_now, e1.get_position(), e2.get_position(), e3.get_position(), e4.get_position(),
                          b1.ret_cord(), b2.ret_cord())):
                e2.set_position(lp1[0], lp1[1])
            lisp.append(e2.get_position())
            lpb = enlisp[random.randrange(4)]
            lp1[0] = lpb[0]
            lp1[1] = lpb[1]
        if(e3.get_life() == 1):
            e3ar = e3.get_position()
            lp1[0] = lp1[0] + e3ar[0]
            lp1[1] = lp[1] + e3ar[1]
            if (check_pos(lp1, board_now, e1.get_position(), e2.get_position(), e3.get_position(), e4.get_position(),
                          b1.ret_cord(), b2.ret_cord())):
                e3.set_position(lp1[0], lp1[1])
            lisp.append(e3.get_position())
            lpc = enlisp[random.randrange(4)]
            lp1[0] = lpc[0]
            lp1[1] = lpc[1]
        if(e4.get_life() == 1):
            e4ar = e4.get_position()
            lp1[0] = lp1[0] + e4ar[0]
            lp1[1] = lp[1] + e4ar[1]
            if (check_pos(lp1, board_now, e1.get_position(), e2.get_position(), e3.get_position(), e4.get_position(),
                          b1.ret_cord(), b2.ret_cord())):
                e4.set_position(lp1[0], lp1[1])
            lisp.append(e4.get_position())

        if(b1.get_life()):
            lisp.append(b1.ret_cord())

        if(b2.get_life()):
            lisp.append(b2.ret_cord())

        if(c == 'd'):
            flagd = 0
            if (board_now[tup_pos[1] - 1][tup_pos[0] - 1 + 4] == 'X'):
                lisp.append(bomberman.get_position())
                flag = 1

            elif (b1.get_life() or b2.get_life()):
                if (b1.get_life()):
                    if(check_d(bomberman.get_position(), b1.ret_cord())):
                        flagd = 1
                        flag = 1
                if (b2.get_life()):
                    if (check_d(bomberman.get_position(), b2.ret_cord())):
                        flagd = 1
                        flag = 1
                if flagd == 1:
                    lisp.append(bomberman.get_position())

                if flagd == 0:
                    bomberman.change_position(4, 0)
                    pos = []
                    pos.append(tup_pos[0] + 4)
                    pos.append(tup_pos[1])
                    lisp.append(pos)
                    flag = 1
            else:
                bomberman.change_position(4, 0)
                pos = []
                pos.append(tup_pos[0] + 4)
                pos.append(tup_pos[1])
                lisp.append(pos)
                flag = 1



        if(c == 'a'):
            flaga = 0
            if board_now[tup_pos[1] - 1][tup_pos[0] - 1 - 4] == 'X':
                lisp.append(bomberman.get_position())
                flag = 1

            elif (b1.get_life() or b2.get_life()):
                if (b1.get_life()):
                    if(check_a(bomberman.get_position(), b1.ret_cord())):
                        flag = 1
                        flaga = 1

                if (b2.get_life()):
                    if (check_a(bomberman.get_position(), b2.ret_cord())):
                        flag = 1
                        flaga = 1
                if flaga == 1:
                    lisp.append(bomberman.get_position())

                if flaga == 0:
                    bomberman.change_position(-4, 0)
                    pos = []
                    pos.append(tup_pos[0] - 4)
                    pos.append(tup_pos[1])
                    lisp.append(pos)
                    flag = 1
            else:
                bomberman.change_position(-4, 0)
                pos = []
                pos.append(tup_pos[0] - 4)
                pos.append(tup_pos[1])
                lisp.append(pos)
                flag = 1


        if(c == 's'):
            flags = 0
            if (tup_pos[1] + 2) >= 1 and tup_pos[1] + 2 <= boa.y_border:
                if board_now[tup_pos[1] - 1 + 2][tup_pos[0] - 1] == 'X':
                    lisp.append(bomberman.get_position())
                    flag = 1
                elif (b1.get_life() or b2.get_life()):
                    if (b1.get_life()):
                        if (check_s(bomberman.get_position(), b1.ret_cord())):
                            flag = 1
                            flags = 1

                    if (b2.get_life()):
                        if (check_s(bomberman.get_position(), b2.ret_cord())):
                            flag = 1
                            flags = 1

                    if flags == 1:
                        lisp.append(bomberman.get_position())

                    if flags == 0:
                        bomberman.change_position(0, 2)
                        pos = []
                        pos.append(tup_pos[0])
                        pos.append(tup_pos[1] + 2)
                        lisp.append(pos)
                        flag = 1
                else:
                    bomberman.change_position(0, 2)
                    pos = []
                    pos.append(tup_pos[0])
                    pos.append(tup_pos[1] + 2)
                    lisp.append(pos)
                    flag = 1

            else:
                lisp.append(bomberman.get_position())
                flag = 1

        if(c == 'w'):
            flagw = 0
            if (tup_pos[1] - 2) >= 1 and (tup_pos[1] - 2) <= boa.y_border:
                if board_now[tup_pos[1] - 1 - 2][tup_pos[0] - 1] == 'X':
                    lisp.append(bomberman.get_position())
                    flag = 1
                elif (b1.get_life() or b2.get_life()):
                    if (b1.get_life()):
                        if (check_w(bomberman.get_position(), b1.ret_cord())):
                            flag = 1
                            flagw = 1
                    if (b2.get_life()):
                        if (check_w(bomberman.get_position(), b2.ret_cord())):
                            flag = 1
                            flagw = 1

                    if flagw == 1:
                        lisp.append(bomberman.get_position())

                    if flagw == 0:
                        bomberman.change_position(0, -2)
                        pos = []
                        pos.append(tup_pos[0])
                        pos.append(tup_pos[1] - 2)
                        lisp.append(pos)
                        flag = 1

                else:
                    bomberman.change_position(0, -2)
                    pos = []
                    pos.append(tup_pos[0])
                    pos.append(tup_pos[1] - 2)
                    lisp.append(pos)
                    flag = 1
            else:
                lisp.append(bomberman.get_position())
                flag = 1

        if c == 'q':
            print('Game quits')
            exit()
        if (e1.get_life() == 1):

            if (check_destroy_enemy(e1.get_position(),
                                    bomberman.get_position())):
                bomberman.Got_killed()
                print(bomberman.get_life())
                if bomberman.get_life() == 0:
                    print('game over')
                    gameexit = True
                    break

                else:
                    bomberman.set_position(5, 3)
            else:
                pass
        else:
            pass
        if bomberman.get_life() == 0:
            break

        if e2.get_life() == 1:

            if (check_destroy_enemy(e2.get_position(),
                                    bomberman.get_position())):
                #lisp.remove(bomberman.get_position())
                bomberman.Got_killed()
                print(bomberman.get_life())
                if bomberman.get_life() == 0:
                    print('game over')
                    gameexit = True
                    break

                else:
                    bomberman.set_position(5, 3)
            else:
                pass
        else:
            pass

        if bomberman.get_life() == 0:
            break
        if e3.get_life() == 1:

            if check_destroy_enemy(e3.get_position(), bomberman.get_position()):

                print(bomberman.get_life())
                bomberman.Got_killed()
                if bomberman.get_life() == 0:
                    print('game over')
                    gameexit = True
                    break

                else:
                    bomberman.set_position(5, 3)
            else:
                pass
        else:
            pass
        if bomberman.get_life() == 0:
            break



        if e4.get_life() == 1:

            if check_destroy_enemy(e4.get_position(), bomberman.get_position()):

                bomberman.Got_killed()
                print(bomberman.get_life())
                if bomberman.get_life() == 0:
                    gameexit = True
                    print('game over')
                    break

                else:
                    bomberman.set_position(5, 3)
            else:
                pass
        else:
            pass

        if bomberman.get_life() == 0:
            break
        if bombframes == 0:
            if c == 'b':
                bombframes += 1
                lisp.append(bomberman.get_position())
                bomb_pos = bomberman.put_bomb()
                lisp.append(bomb_pos)
                boa.update_board(lisp, n, 0, br)
                continue
            else:
                pass


        if bombframes == 1 or bombframes == 2 or bombframes == 3:
            bombframes += 1
            if flag == 0:
                lisp.append(bomberman.get_position())
            lisp.append(bomb_pos)
            boa.update_board(lisp, n, 0, br)
            continue
        else:
            pass

        if bombframes == 4:

            bombframes = 0
            if (e1.get_life() == 1):
                if(check_destroy(e1.get_position(), bomb_pos)):
                    lisp.remove(e1.get_position())
                    e1.Kill_by_bomb()
                    n -= 1
                    print('Enemy killed')
                    bomberman.inc_score()
                    if n == 0:
                        print('Congratulation for level up')
                        print('Final score : ' + str(bomberman.get_score()))
                        bomberman.inc_level()
                        exit()

                else:
                    pass
            else:
                pass
            if (b1.get_life()):
                if (check_destroy(b1.ret_cord(), bomb_pos)):
                    lisp.remove(b1.ret_cord())
                    b1.destroy()
                    br -= 1
                    bomberman.inc_brick_score()

            if (b2.get_life()):
                if (check_destroy(b2.ret_cord(), bomb_pos)):
                    lisp.remove(b2.ret_cord())
                    b2.destroy()
                    br -= 1
                    bomberman.inc_brick_score()

            if e2.get_life() == 1:
                if(check_destroy(e2.get_position(), bomb_pos)):
                    lisp.remove(e2.get_position())
                    e2.Kill_by_bomb()
                    n -= 1
                    print('enemy killed')

                    bomberman.inc_score()
                    if n == 0:
                        print('Congratulations for level up')
                        print('Final score : ' + str(bomberman.get_score()))
                        bomberman.inc_level()
                        exit()
                else:
                    pass
            else:
                pass
            if (e3.get_life() == 1):
                if(check_destroy(e3.get_position(), bomb_pos)):
                    lisp.remove(e3.get_position())
                    e3.Kill_by_bomb()
                    n -= 1
                    print('enemy killed')

                    bomberman.inc_score()
                    if n == 0:
                        print('Congratulations for level up')
                        print('Final score : ' + str(bomberman.get_score()))
                        bomberman.inc_level()
                        exit()
                else:
                    pass
            else:
                pass

            if (e4.get_life() == 1):
                if(check_destroy(e4.get_position(), bomb_pos)):
                    lisp.remove(e4.get_position())
                    e4.Kill_by_bomb()
                    n -= 1
                    print('enemy killed')

                    bomberman.inc_score()
                    if n == 0:
                        print('Congratulations for level up')
                        print('Final score : ' + str(bomberman.get_score()))
                        bomberman.inc_level()
                        exit()
                else:
                    pass
            else:
                pass

            if n == 0:
                bomberman.inc_level()
                print('Congratulation for Level-UP')
                print('Final score : ' + str(bomberman.get_score()))
                break
            if (bomberman.get_life() >= 0):
                if(check_destroy(bomberman.get_position(), bomb_pos)):

                    bomberman.Got_killed()
                    if bomberman.get_life() == 0:
                        print('game over')
                        gameexit = True
                        break

                    else:
                        bomberman.set_position(5, 3)
                else:
                    pass
            else:
                pass

            if flag == 0:
                lisp.append(bomberman.get_position())
            boa.update_board(lisp, n, 1, br)
            bomb_pos = None
        else:
            pass

        if bomberman.get_life() == 0:
            break
        if n == 0:
            print('Congratulations level up')
            print('Final score : ' + str(bomberman.get_score()))
            bomberman.inc_level()
            exit()

        if bombframes == 0:
            if flag == 0:
                lisp.append(bomberman.get_position())

            boa.update_board(lisp, n, 0, br)



    return 0


def check_destroy(l1, l2):
    if l1[0] == l2[0]:
        if (l2[1] == l1[1] - 2) or (l2[1] == l1[1] + 2) or (l2[1] == l1[1]):
            return True
    elif l1[1] == l2[1]:
        if (l2[0] == l1[0] + 4) or (l2[0] == l1[0] - 4) or (l2[0] == l1[0]):
            return True
    else:
        return False

def check_destroy_enemy(l1, l2):
    if(l1[0] == l2[0]) and (l1[1] == l2[1]):
        return True
    else:
        return False
def check_a(l1, l2):
    if l1[1] == l2[1]:
        if l1[0] - 4 == l2[0]:
            return True
        else:
            return False
    else:
        return False

def check_d(l1, l2):
    if l1[1] == l2[1]:
        if l1[0] + 4 == l2[0]:
            return True
        else:
            return False
    else:
        return False

def check_w(l1, l2):
    if l1[0] == l2[0]:
        if l1[1]-2 == l2[1]:
            return True
        else:
            return False
    else:
        return False

def check_s(l1, l2):
    if l1[0] == l2[0]:
        if l1[1]+2 == l2[1]:
            return True
        else:
            return False
    else:
        return False

print(str(gameexit) + 'gameexit')
if not gameexit:
    k = startgame()
