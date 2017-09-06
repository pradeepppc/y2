from Enemy import *
from Bomberman import *
from Bomb import *
import numpy as np
import os
import getch



class Board():

    x_border = 76
    y_border = 44
    board = []
    def __init__(self,x,y):
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
            if (i>= 0 and i <= 3) or (i>= self.x_border - 4 and i<= self.x_border - 1):
                l2.append('X')
            else:
                l2.append(' ')
        k = 0
        i = 0
        for i in range(self.x_border):
            if (k>=0 and k<=3):
                l3.append('X')
                k += 1
                continue
            elif (k>=4 and k<=7):
                l3.append(' ')
                k += 1
                if(k == 8):
                    k =0
        h = 0
        i = 0
        for i in range(self.y_border):
            if (i>=0 and i<=1) or (i == self.y_border -2 or i == self.y_border -1):
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
                        h =0
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
        for i in range(self.y_border):
            x = ''
            for k in range(self.x_border):
                x += str(board_arr[i][k])
            print(x)

    def update_board(self,lisp,n,flag):
                board_arr = self.printBoard()
                for j in range(4):
                    for k in range(n):
                        board_arr[lisp[k][1] - 1][lisp[k][0] -1 +j] = 'E'
                        board_arr[lisp[k][1]][lisp[k][0] -1 +j] = 'E'

                    board_arr[lisp[n][1]-1][lisp[n][0]-1+j] = 'B'
                    board_arr[lisp[n][1]][lisp[n][0]+j-1] = 'B'
                    if ( len(lisp) == n+2):
                        if flag == 0:
                            board_arr[lisp[n+1][1] - 1][lisp[n+1][0] - 1 + j] = 'O'
                            board_arr[lisp[n+1][1]][lisp[n+1][0] + j - 1] = 'O'
                        else:
                            board_arr[lisp[n + 1][1] - 1][lisp[n + 1][0] - 1 + j] = 'e'
                            board_arr[lisp[n + 1][1]][lisp[n + 1][0] + j - 1] = 'e'


                for i in range(self.y_border):
                    x = ''
                    for k in range(self.x_border):
                        x += str(board_arr[i][k])
                    print(x)


bomberman = Bomberman()
gameexit = False

def startgame():
    boa = Board(76,44) #creating board
     #creating bomberman
    e1 = Enemy()
    e2 = Enemy()
    e3 = Enemy()
    e4 = Enemy()
    e1.set_position(45,5)
    e2.set_position(45,27)
    e3.set_position(29,17)
    e4.set_position(37,29+8)
    bomberman.set_position(5,3)#initial position of bomberman

    boa.printb()
    #os.system('clear')
    lop = 0
    bombframes = 0
    bomb_pos = []
    n = 4
    while True:
        print('Number of lives remaining are :' + ' ' +  str(bomberman.get_life())+ '                      ' + 'SCORE : ' +
              str(bomberman.get_score()))

        flag = 0
        #os.system('clear')
        #c = str(raw_input('enter'))
        c = getch.getch()
        tup_pos = bomberman.get_position()

        board_now = boa.printBoard()
        lisp = []
        if lop == 0:
            e1.set_position(45,3)
            e3.set_position(29,15)
            e2.set_position(41,27)
            lop += 1
        elif lop == 1:
            e1.set_position(45,5)
            e3.set_position(29,17)
            e2.set_position(45,27)
            lop += 1
        else:
            e1.set_position(45,7)
            e3.set_position(29,19)
            e2.set_position(49,27)
            lop = 0
        if(e1.get_life() == 1):

            lisp.append(e1.get_position())
        if(e2.get_life() == 1):
            lisp.append(e2.get_position())
        if(e3.get_life() == 1):
            lisp.append(e3.get_position())
        if(e4.get_life() == 1):
            lisp.append(e4.get_position())
        if(c == 'd'):
            if board_now[tup_pos[1]-1][tup_pos[0]-1+4] == 'X':
                lisp.append(bomberman.get_position())
                flag = 1


            else:
                bomberman.change_position(4,0)
                pos = []
                pos.append(tup_pos[0]+4)
                pos.append(tup_pos[1])
                lisp.append(pos)
                flag = 1



        if(c == 'a'):
            if board_now[tup_pos[1]-1][tup_pos[0]-1-4] == 'X':
                lisp.append(bomberman.get_position())
                flag = 1


            else:
                bomberman.change_position(-4,0)
                pos = []
                pos.append(tup_pos[0]-4)
                pos.append(tup_pos[1])
                lisp.append(pos)
                flag = 1


        if(c == 's'):
            if (tup_pos[1]+ 2) >= 1 and (tup_pos[1] + 2 ) <= boa.y_border:
                if board_now[tup_pos[1]-1 + 2][tup_pos[0]-1] == 'X':
                    lisp.append(bomberman.get_position())
                    flag = 1
                else:
                    bomberman.change_position(0,2)
                    pos = []
                    pos.append(tup_pos[0])
                    pos.append(tup_pos[1] + 2)
                    lisp.append(pos)
                    flag = 1

            else:
                lisp.append(bomberman.get_position())
                flag = 1

        if(c == 'w'):
            if (tup_pos[1] - 2) >= 1 and (tup_pos[1] - 2 ) <= boa.y_border:
                if board_now[tup_pos[1]-1 - 2][tup_pos[0]-1] == 'X':
                    lisp.append(bomberman.get_position())
                    flag = 1
                else:
                    bomberman.change_position(0,-2)
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

            if (check_destroy_enemy(e1.get_position(), bomberman.get_position())):
                bomberman.Got_killed()
                print(bomberman.get_life())
                if bomberman.get_life() == 0:
                    print('game over')
                    gameexit = True
                    break

                else:
                    bomberman.set_score(0)
                    startgame()
            else:
                pass
        else:
            pass
        if bomberman.get_life() == 0:
            break

        if(e2.get_life() == 1):

            if (check_destroy_enemy(e2.get_position(), bomberman.get_position())):
                #lisp.remove(bomberman.get_position())
                bomberman.Got_killed()
                print(bomberman.get_life())
                if bomberman.get_life() == 0:
                    print('game over')
                    gameexit =True
                    break

                else:
                    bomberman.set_score(0)
                    startgame()
            else:
                pass
        else:
            pass

        if bomberman.get_life() == 0:
            break
        if (e3.get_life() == 1):

            if (check_destroy_enemy(e3.get_position(), bomberman.get_position())):

                print(bomberman.get_life())
                bomberman.Got_killed()
                if bomberman.get_life() == 0:
                    print('game over')
                    gameexit =True
                    break

                else:
                    bomberman.set_score(0)
                    startgame()
            else:
                pass
        else:
            pass
        if bomberman.get_life() == 0:
            break



        if (e4.get_life() == 1):

            if (check_destroy_enemy(e4.get_position(), bomberman.get_position())):

                bomberman.Got_killed()
                print(bomberman.get_life())
                if bomberman.get_life() == 0:
                    gameexit = True
                    print('game over')
                    break

                else:
                    bomberman.set_score(0)
                    startgame()
            else:
                pass
        else:
            pass

        if bomberman.get_life() == 0:
            break

        if c == 'b':
            bombframes += 1
            lisp.append(bomberman.get_position())
            bomb_pos = bomberman.put_bomb()
            lisp.append(bomb_pos)
            boa.update_board(lisp,n,0)
            continue
        else:
            pass


        if bombframes == 1 or bombframes == 2 or bombframes == 3:
            bombframes += 1
            if flag == 0:
                lisp.append(bomberman.get_position())
            lisp.append(bomb_pos)
            boa.update_board(lisp,n,0)
            continue
        else:
            pass

        if bombframes == 4:

            bombframes = 0
            if (e1.get_life() == 1):
                if(check_destroy(e1.get_position(),bomb_pos)):
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

            if (e2.get_life() == 1):
                if(check_destroy(e2.get_position(),bomb_pos)):
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
                if(check_destroy(e3.get_position(),bomb_pos)):
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
                if(check_destroy(e4.get_position(),bomb_pos)):
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
                if(check_destroy(bomberman.get_position(),bomb_pos)):

                    bomberman.Got_killed()
                    if bomberman.get_life() == 0:
                        print('game over')
                        gameexit = True
                        break

                    else:
                        startgame()
                else:
                    pass
            else:
                pass

            if flag == 0:
                lisp.append(bomberman.get_position())
            boa.update_board(lisp,n,1)
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

            boa.update_board(lisp,n,0)



    return 0


def check_destroy(l1,l2):
    if l1[0] == l2[0]:
        if ((l2[1] == l1[1] - 2) or (l2[1] == l1[1] + 2) or (l2[1] == l1[1])):
            return True
    elif l1[1] == l2[1]:
        if ((l2[0] == l1[0] + 4) or (l2[0] == l1[0] - 4) or (l2[0] == l1[0])):
            return True
    else:
        return False

def check_destroy_enemy(l1,l2):
    if(l1[0] == l2[0]) and (l1[1] == l2[1]):
        return True
    else:
        return False


print(str(gameexit) + 'gameexit')
if gameexit == False:
    k = startgame()
