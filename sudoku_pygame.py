import pygame
from pygame.locals import *
import time
import pathlib
import gen_grid
import numpy
path = str(pathlib.Path(__file__).parent.resolve())

#variables
squares = 10
mouse_pos = (0,0)
move = (numpy.inf, numpy.inf)


#CONSTANTS 
WIDTH, HEIGHT = 650,650
XSPACE = WIDTH//9
YSPACE = HEIGHT//9
XS = WIDTH//18
YS = HEIGHT//18

WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
RED = (255,0,0)
GREEN = (0,255,0)
CRIMSON = (220,20,60)

KEYS = {K_KP1: 1, K_KP2: 2, K_KP3: 3, K_KP4: 4, K_KP5: 5, K_KP6: 6, K_KP7: 7, K_KP8: 8, K_KP9: 9,}

REMOVE = 20

#getting argument for pygame.draw.line for drawing grid
row_lines = []
column_lines = []
for i in range(squares):
    row_lines.append((0, int(i*XSPACE)))
    column_lines.append((int(i*YSPACE), 0))


#INIT
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SUDOKU")
pygame.font.init()
num_font = pygame.font.SysFont("comicsans", 40)
notify_font = pygame.font.SysFont("comicsans", 80)
board, r_board = gen_grid.generate(REMOVE)

#func definition

def draw_num():
    xs = XS 
    ys = YS
    #drawing numbers on grid
    for line in r_board:
        for num in line:
            if num == 0:
                text = num_font.render(" ", 1, YELLOW)
            else:
                text = num_font.render(str(num), 1, YELLOW)
            screen.blit(text, (xs-text.get_width()//2, ys-text.get_height()//2))
            
            xs += XS*2 
        ys += YS*2
        xs = XS 

def draw(valid, rec_x, rec_y, guess_right, notify, mistakes, nums_pos, win):
    screen.fill(BLACK)
    #drawing grid
    for i, j in zip(row_lines, column_lines):
        pygame.draw.line(screen, WHITE, i, (WIDTH, i[1]), 1)
        pygame.draw.line(screen, WHITE, j, (j[0], HEIGHT), 1)

    #drawing lines which seperate 3x3 grids
    for i in 3,6:
        r = row_lines[i]
        c = column_lines[i]
        pygame.draw.line(screen, WHITE, r, (WIDTH, r[1]), 5)
        pygame.draw.line(screen, WHITE, c, (c[0], HEIGHT), 5)
    draw_num()
    if valid:
        #drawing green rectangles on positions with same number as selected
        for x, y in nums_pos:
            pygame.draw.rect(screen, GREEN, (x, y, XSPACE, YSPACE),3)
        #draw red or green rectangle on selected position
        if guess_right:
            pygame.draw.rect(screen, GREEN, (rec_x, rec_y, XSPACE, YSPACE),3)
        else:
            pygame.draw.rect(screen, RED, (rec_x, rec_y, XSPACE, YSPACE),3)

    if notify:
        #drawing notifications
        if mistakes != 0:
            notify_text = notify_font.render(f"{mistakes} mistakes left", 1, CRIMSON)
            screen.blit(notify_text, (WIDTH//2 - notify_text.get_width()//2, HEIGHT//2 - notify_text.get_height()//2))
        else:
            notify_text = notify_font.render("GAME OVER", 1, CRIMSON)
            screen.blit(notify_text, (WIDTH//2 - notify_text.get_width()//2, HEIGHT//2 - notify_text.get_height()//2))
        
    if win:
        notify_text = notify_font.render("You won", 1, GREEN)
        screen.blit(notify_text, (WIDTH//2 - notify_text.get_width()//2, HEIGHT//2 - notify_text.get_height()//2))

    pygame.display.update()
    if notify or win:
        time.sleep(2)


def get_rc(pos):
    #when you press mouse this func determines on what you clicked
    #return row and column num. eg: (0,5) [first row, sixth column]
    x = pos[0]
    y = pos[1]

    valid = True
    row = numpy.inf
    column = numpy.inf

    for i in range(squares):
        tup_1 = row_lines[i]
        tup_2 = row_lines[i+1]
        if y > tup_1[1] and  y < tup_2[1]:
            row = int(i)       
            break

    for i in range(squares):
        tup_1 = column_lines[i]
        tup_2 = column_lines[i+1]
        if x > tup_1[0] and  x < tup_2[0]:
            column = int(i)
            break

    #checking if the value is valid
    if type(row) != int or type(column) != int:
        valid = False

    tup = (row, column)
    return valid, tup

def get_same_num(move):
    #this func determines which squares has same number on it as seletected one does
    selected_num = r_board[move[0]][move[1]]
    

    num_pos = []
    for r, line in enumerate(r_board):
        for c, n in enumerate(line):
            if n == selected_num and selected_num != 0:
                m = (r, c)
                num_pos.append((column_lines[m[1]][0], row_lines[m[0]][1]))

    
    return num_pos

def check_win():
    #checks if player has completed the sudoku
    win = True
    for line in r_board:
        for num in line:
            if num == 0:
                win = False

    return win

def main():
    run = True
    selected = False
    valid = False
    guess_right = True
    notify = False
    win = False

    rec_x = 0
    rec_y = 0
    num = None
    mistakes = 3
    nums_pos = []
    while run:
        notify = False
        #if you make 3 mistakes game ends
        if mistakes == 0 or win:
           run = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                guess_right = True
                try:
                    valid, move = get_rc(mouse_pos)
                    nums_pos = get_same_num(move)
                    num = r_board[move[0]][move[1]]
                    rec_x = column_lines[move[1]][0]
                    rec_y = row_lines[move[0]][1]
                    selected = True
                except:
                    print("invalid value")
                    selected = False

            #TRY TO THINK OF SOMETHING BETTER WHICH WOULD USE THAT DICTIONARY UP THERE
            if event.type == pygame.KEYDOWN and selected and num == 0:
                key = None
                if event.key == K_KP1: key = 1
                if event.key == K_KP2: key = 2
                if event.key == K_KP3: key = 3
                if event.key == K_KP4: key = 4
                if event.key == K_KP5: key = 5
                if event.key == K_KP6: key = 6
                if event.key == K_KP7: key = 7
                if event.key == K_KP8: key = 8
                if event.key == K_KP9: key = 9
            
                #print(board[move[0]][move[1]])
                if key is not None:
                    if board[move[0]][move[1]] == key:
                        r_board[move[0]][move[1]] = key     
                    else:
                        notify = True
                        guess_right = False
                        mistakes -= 1
                else:
                    print("Invalid key input.")
            
        win = check_win()
        draw(valid, rec_x, rec_y, guess_right, notify, mistakes, nums_pos, win)

main()
pygame.quit()

