import random
import copy

base  = 3
side  = base*base
#remove = 10
removed = []

# pattern for a baseline valid solution
def pattern(r,c): 
    return (base*(r%base)+r//base+c)%side

# randomize rows, columns and numbers (of valid base pattern)
def shuffle(s): 
    return random.sample(s,len(s)) 


def generate(remove):
    r_base = range(base) 

    rows  = [ g*base + r for g in shuffle(r_base) for r in shuffle(r_base) ] 
    cols  = [ g*base + c for g in shuffle(r_base) for c in shuffle(r_base) ]

    nums  = shuffle(range(1,base*base+1))

    # produce board using randomized baseline pattern
    board = [ [nums[pattern(r,c)] for c in cols] for r in rows ]

    r_board = copy.deepcopy(board)
    
    #handle repetition
    r_list = []
    while len(r_list) != remove:
        for i in range(remove - len(r_list)):
            tup = (random.randrange(0,9), random.randrange(0,9))

            if tup not in r_list:
                r_list.append(tup)

    for i, j in r_list:
        r_board[i][j] = 0

    return board, r_board



#board, r_board = generate(10)

def get_optins(s_pos, r_board):
    used_nums = []
    options = []
    #row
    for s in r_board[s_pos[0]]:
        if s != 0 and s not in used_nums:
            used_nums.append(s)

    #column
    for i in range(9):
        s = r_board[i][s_pos[1]]
        if s != 0 and s not in used_nums:
            used_nums.append(s)

    #square 3x3
    if s_pos[0]%3 == 0: x = int(s_pos[0])
    if s_pos[0]%3 == 1: x = int(s_pos[0])-1 
    if s_pos[0]%3 == 2: x = s_pos[0]-2

    if s_pos[1]%3 == 0: y = int(s_pos[1])
    if s_pos[1]%3 == 1: y = int(s_pos[1])-1
    if s_pos[1]%3 == 2: y = int(s_pos[1])-2
    
    iter_pos = (x,y)

    for i in range(3):
        for j in range(3):
            s = r_board[iter_pos[0]+i][iter_pos[1]+j]
            if s != 0 and s not in used_nums:
                used_nums.append(s)

    #print(used_nums)
    #print(iter_pos)

    for i in range(1,10):
        if i not in used_nums:
            options.append(i)

    return options

def get_hint_board(r_board):
    hint_board = copy.deepcopy(r_board)
    options = []
    for x, row in enumerate(hint_board):
        for y, s in enumerate(row):
            if s == 0:
                options = get_optins((x,y), r_board)
                hint_board[x][y] = options
            options = []

    return hint_board


