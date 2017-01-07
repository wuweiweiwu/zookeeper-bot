from PIL import ImageGrab
import numpy
from image_recognizer import Recognizer
import pyautogui as control
from copy import deepcopy
import time
import sys

'''coordinates of the box'''
'''mac dpi multiply location by 2'''
# board_box = (995*2, 275*2, 1542*2, 831*2)
board_box = (1035, 357, 1500, 835)
board_box = tuple([z * 2 for z in board_box])
board_size = 8
img_size = (board_box[2]-board_box[0], board_box[3]-board_box[1])
cell_size = (img_size[0]/board_size, img_size[1]/board_size)

game_board = numpy.zeros((board_size, board_size), dtype=numpy.int32)
recognizer = Recognizer()


def click(coor):
    control.click(x=coor[0], y=coor[1], button='left', clicks=1)


def get_coords(cell):
    x = board_box[0] + cell[1]*cell_size[0] + cell_size[0]/2
    y = board_box[1] + cell[0]*cell_size[1] + cell_size[1]/2
    # print x
    # print y
    return x/2, y/2


def do_move(move):
    print 'move: ',
    print move
    start = get_coords(move[0])
    end = get_coords(move[1])
    click(start)
    click(end)


def print_board():
    for line in game_board:
        for elem in line:
            print elem,
            print ' ',
        print


def fill_board():
    img = ImageGrab.grab()
    # img.save('desktop.png','PNG')
    img = img.crop(board_box)
    # img.save('board.png', 'PNG')

    for x in range(0, 8):
        for y in range(0, 8):
            cell_box = (x*cell_size[0], y*cell_size[1], (x+1)*cell_size[0], (y+1)*cell_size[1])
            cell = img.crop(cell_box)
            # name = 'x' + str(x) + 'y' + str(y) + '.png'
            # cell.save(name, 'PNG')
            game_board[y][x] = recognizer.predict(cell)


def has_match(board):
    for x in range(7, -1, -1):
        for y in range(7, -1, -1):
            if 0 <= x < board_size and 0 <= x+1 < board_size and 0 <= x+2 < board_size:
                if board[x][y] == board[x+1][y] == board[x+2][y]:
                    return True
            if 0 <= y < board_size and 0 <= y+1 < board_size and 0 <= y+2 < board_size:
                if board[x][y] == board[x][y+1] == board[x][y+2]:
                    return True
    return False


def get_move():
    for x in range(7, -1, -1):
        for y in range(7, -1, -1):
            board = deepcopy(game_board)
            if 0 <= x < board_size and 0 <= y < board_size and 0 <= x+1 < board_size:
                board[x][y], board[x+1][y] = board[x+1][y], board[x][y]
                if has_match(board):
                    start = (x, y)
                    end = (x+1, y)
                    # do_move((start, end))
                    return start, end
            board = deepcopy(game_board)
            if 0 <= x < board_size and 0 <= y < board_size and 0 <= y + 1 < board_size:
                board[x][y], board[x][y+1] = board[x][y+1], board[x][y]
                if has_match(board):
                    start = (x, y)
                    end = (x, y+1)
                    # print game_board[x][y]
                    # print game_board[x][y+1]
                    # do_move((start, end))
                    return start, end


def play():
    recognizer.train()
    total_num_sec = input('Enter number of seconds to run: ')
    end_time = time.time() + total_num_sec
    while time.time() < end_time:
        fill_board()
        print_board()
        move = get_move()
        do_move(move)
        time.sleep(2)


if __name__ == '__main__':
    play()